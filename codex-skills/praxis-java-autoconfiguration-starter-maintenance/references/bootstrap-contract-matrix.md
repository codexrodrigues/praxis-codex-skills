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
