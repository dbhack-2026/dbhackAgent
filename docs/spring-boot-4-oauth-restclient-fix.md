# Spring Boot 4: OAuth token client and load-balanced `RestClient` fix

## Problem

The application used a single `RestClient.Builder` annotated with `@LoadBalanced` for both service-to-service calls and OAuth token retrieval.

When the OAuth token URI was an absolute infrastructure URL such as:

```text
https://uat2-eureka.intranet.db.com/...
```

Spring Cloud LoadBalancer interpreted the hostname as a logical service ID and attempted to resolve it through Eureka. Because Eureka itself was still being initialized, startup failed with errors such as:

```text
No servers available for service: uat2-eureka.intranet.db.com
Service Instance cannot be null
BeanCurrentlyInCreationException: scopedTarget.eurekaClient
```

## Final configuration

Use separate direct and load-balanced builders.

```java
package com.db.awmd.trade.config;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.web.client.RestClient;

@Configuration
public class RestClientConfig {

    @Bean
    @Primary
    @Qualifier("directRestClientBuilder")
    public RestClient.Builder directRestClientBuilder() {
        return RestClient.builder();
    }

    @Bean
    @LoadBalanced
    @Qualifier("loadBalancedRestClientBuilder")
    public RestClient.Builder loadBalancedRestClientBuilder() {
        return RestClient.builder();
    }
}
```

Use the direct builder for the OAuth token endpoint:

```java
@Bean
public OAuth2AccessTokenResponseClient<OAuth2ClientCredentialsGrantRequest>
tokenResponseClient(
        @Qualifier("directRestClientBuilder") RestClient.Builder builder,
        ObjectMapper objectMapper) {

    return new CustomClientCredentialsTokenResponseClient(
        builder,
        objectMapper
    );
}
```

The token client should build a direct `RestClient` once:

```java
public final class CustomClientCredentialsTokenResponseClient
        implements OAuth2AccessTokenResponseClient<OAuth2ClientCredentialsGrantRequest> {

    private final RestClient restClient;
    private final ObjectMapper objectMapper;

    public CustomClientCredentialsTokenResponseClient(
            RestClient.Builder directBuilder,
            ObjectMapper objectMapper) {
        this.restClient = directBuilder.build();
        this.objectMapper = objectMapper;
    }

    @Override
    public OAuth2AccessTokenResponse getTokenResponse(
            OAuth2ClientCredentialsGrantRequest grantRequest) {

        ClientRegistration registration = grantRequest.getClientRegistration();

        MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
        form.add("grant_type", "client_credentials");
        if (!registration.getScopes().isEmpty()) {
            form.add("scope", String.join(" ", registration.getScopes()));
        }

        String responseBody = restClient.post()
            .uri(registration.getProviderDetails().getTokenUri())
            .headers(headers -> {
                headers.setBasicAuth(
                    registration.getClientId(),
                    registration.getClientSecret()
                );
                headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
            })
            .body(form)
            .retrieve()
            .body(String.class);

        return parseResponse(responseBody);
    }
}
```

Only clients that use Eureka service names should inject:

```java
@Qualifier("loadBalancedRestClientBuilder")
RestClient.Builder builder
```

## JPA setting

Keep Open EntityManager in View disabled for the REST service:

```yaml
spring:
  jpa:
    open-in-view: false
```

This prevents database access during response rendering and removes the `openEntityManagerInViewInterceptor` startup dependency path.

## Validation checklist

1. Confirm the OAuth token request no longer passes through `DeferringLoadBalancerInterceptor` or `RetryLoadBalancerInterceptor`.
2. Confirm no log reports `No servers available for service: <token-hostname>`.
3. Confirm Eureka initializes successfully.
4. Confirm Hazelcast OCP4 discovery completes after Eureka is available.
5. Confirm the Aladdin Feign interceptor acquires a token only when an outbound request is executed.
6. Run application context and OAuth client integration tests before deployment.
