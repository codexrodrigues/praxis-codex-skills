# Bootstrap Contract Matrix

| Change | Required evidence |
| --- | --- |
| New auto-configuration | Imports registration, default context, conditional behavior |
| New default bean | Unique canonical facade and intended override path |
| SPI extension | Provider/implementation ordering, ambiguity failure, host integration |
| Property | Typed binding, default, validation, public behavior impact |
| Public metadata behavior | Schema/HTTP proof plus direct consumer review |

Never introduce a second public facade bean to satisfy one host. Prefer a named
SPI and ordered provider or a clearly documented override condition.

## Springdoc Response Generation

When maintaining Metadata's Springdoc 2.6 response builder, inspect
`openapi/GenerationScopedGenericResponseService.java`,
`configuration/OpenApiResponseGenerationAutoConfiguration.java`, and
`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`.
The adapter delegates the public `buildGenericResponse` and `build` operations to
a fresh `GenericResponseService` per generation; do not copy Springdoc's parsing
algorithm, reflectively clear its private lists, or disable generic error responses.

1. Verify imports registration and ordering after `SpringDocConfiguration` and
   before `SpringDocWebMvcConfiguration`. Require the core configuration bean,
   the relevant classes, a servlet application, and enabled API docs (enabled by
   default). Class presence alone does not prove that the host enabled the core.
   Also inspect `PraxisMetadataAutoConfiguration`: its two static `GroupedOpenApi`
   definitions must precede `SpringDocConfiguration` during bean registration.
   Springdoc 2.6 conditionally registers `springdocBeanFactoryPostProcessor` only
   when its REGISTER_BEAN condition sees grouped definitions (or the supported
   cache-disabled path). Keep registered auto-configurations out of the principal
   `@ComponentScan` with Boot's `AutoConfigurationExcludeFilter`; they belong to
   `AutoConfiguration.imports`, whose ordering and conditions must remain in charge.
   Inventory every excluded auto-configuration against that manifest before editing.
   Preserve ordinary scanned configuration such as `DynamicSwaggerConfig`. Merely
   moving the principal configuration before the core while scanning the response
   auto-configuration early can satisfy prototype scope but skip the response
   adapter's core-presence condition. Require both guarantees in the same context.
   That processor makes `OpenAPIService` prototype. An
   ordering edge that moves the core ahead of these definitions can leave the
   builder singleton; its locale cache then returns the first group's document
   for another group. Dynamically registered PostConstruct groups are too late
   to prove this condition. Preserve the canonical ordering edge rather than
   disabling the response adapter, generic responses or cache in a host.
2. Preserve `@ConditionalOnMissingBean(GenericResponseService.class)`. A host
   override remains authoritative; do not install a competing builder. Keep the
   adapter's concrete `@Bean` return type so the same bean is discoverable as a
   `GlobalOpenApiCustomizer`.
3. Keep generic preparation and operation builds on the same thread and the
   same `Components` object identity, not merely equal component contents.
   Explicitly disabled generic responses use a fresh empty delegate without
   requiring a prepared frame; they must not borrow another generation's advice.
4. Release servlet frames in the global callback after path generation or at
   request completion. There is no fixed servlet frame-count cap. Ordering last
   among globals does not mean last among all customizers: group customizers can
   run afterward and must not reinvoke the builder after release. Non-servlet
   calls retain at most one frame per thread, replaced by the next generation;
   do not promise arbitrary nested generations or cross-thread continuation.
5. Run `OpenApiResponseGenerationAutoConfigurationTest` and
   `GenerationScopedGenericResponseServiceTest`. Use real MVC auto-configuration
   in the context runner (including `mvcConversionService`), and prove default,
   host override, absent core, non-servlet, and disabled-docs conditions.
   Response fixtures must call `MethodAttributes.calculateConsumesProduces`
   before operation builds and declare exception-handler media types when
   asserting them: Springdoc's generic default is `*/*`, and method-level
   `@RequestMapping(produces = "application/json")` establishes JSON explicitly.
   `ReturnTypeParser` 2.6 is not a functional interface; use a concrete instance.
   Compare complete `ApiResponses` and `Components` against the original service,
   including success and global/local error refs, repeated generations, isolated
   concurrent groups, disabled generics, and cleanup after observable failures.

Prove grouping with the default enabled Springdoc cache in
`OpenApiGroupRegistrationE2ETest`: require the processor, the actual
`openAPIBuilder` prototype scope and the canonical response adapter, then read
multiple real HTTP group documents and require their own paths and absence of
another group's paths. Pair this with the resource unit-delete OpenAPI test;
run the discovery/schema/capability consumers affected by the ordering edge.
A synthetic context or HTTP200 alone cannot prove group isolation. When a
failure appears only in a full suite, preserve its document and test order,
then compare focused cases before blaming a removed route or rewriting asserts.
Recheck absent core, disabled docs and host overrides with the response
bootstrap tests. A cache-disabled reference host proof does not replace this
cache-enabled default proof.

Also inspect `OpenApiUiSchemaAutoConfiguration.modelResolver`: keep its explicit
`@Order(Ordered.HIGHEST_PRECEDENCE)`. Springdoc's `ModelConverterRegistrar`
iterates the injected list, while Swagger's `ModelConverters.addConverter`
prepends each entry. Registration first therefore places the terminal
`CustomOpenApiResolver` after Springdoc decorators and before the plain Swagger
`ModelResolver` in the effective chain. Do not rely on incidental bean-definition
order: introducing an auto-configuration ordering edge can move the resolver
ahead of wrapper/file converters and change schemas as well as generation cost.

Run `OpenApiModelConverterOrderingTest` with two actual bean-definition orders,
using the canonical bean and annotations rather than an ordered fixture copy.
Require `ResponseSupportConverter`, `FileSupportConverter`, and
`AdditionalModelsConverter` before the custom resolver, then the plain resolver.
Prove that `ResponseEntity<DTO>` resolves the DTO, preserves `x-ui` and error refs,
and matches the original response builder. Restore the process-global converter
registry after the test. The focal Metadata classpath lacks Reactor, so it does
not prove `WebFluxSupportConverter` placement; require that decorator before the
custom resolver in the real host where Reactor is present.

A direct non-HTTP one-frame test does not prove the complete Springdoc preload
flow. Verify actual grouped-resource wiring and document parity separately in
the identified host artifact. Do not switch off `springdoc.cache.disabled=true`
to hide accumulation in a host whose governed lifecycle requires fresh sources.
