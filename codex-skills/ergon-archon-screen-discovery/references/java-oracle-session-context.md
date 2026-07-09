# Java Oracle Session Context

Use this reference when a legacy screen query depends on Oracle package state, especially `HADES.FLAG_PACK`.

## Why It Matters

Legacy Ergon/Archon screens often rely on package variables stored in the current Oracle session:

- `flag_pack.get_usuario`
- `flag_pack.get_transacao`
- `flag_pack.get_empresa`

In a Java API with a connection pool, this state belongs to the physical database connection, not to the HTTP request by itself. A migrated API must set the context on the same Oracle connection that will execute the legacy-compatible query.

## Required Discovery Output

For each screen that uses package context, document:

| Item | Required Evidence |
| --- | --- |
| User source | how the authenticated API identity maps to legacy `USUARIO` |
| Transaction code | screen transaction, for example `ERGadm00189` |
| Company source | selector, header, token claim, default, or not applicable |
| Package setters | exact calls needed before the query |
| Package readers | functions used by SQL, views, triggers, packages, or helpers |
| Same-connection strategy | how Java guarantees setters and query use one physical Oracle session |
| Cleanup strategy | how package state is overwritten or cleared before connection reuse |
| Parity cases | privileged, non-privileged allowed, non-privileged denied, company-scoped |

## Recommended First-Pass Strategy

For parity-first migration, prefer setting the Oracle package context before executing legacy-compatible SQL:

```sql
begin
  HADES.FLAG_PACK.SET_USUARIO(:usuario);
  HADES.FLAG_PACK.SET_TRANSACAO(:transacao);
  HADES.FLAG_PACK.SET_EMPRESA(:empresa);
end;
/
```

Use `null` for `empresa` only when the legacy screen is proven to run without a selected company or when the legacy combo intentionally depends on `FLAG_PACK.GET_EMPRESA is null`.

Keep security predicates such as:

```sql
mostra_freq(flag_pack.get_usuario, f.tipofreq, f.codfreq) = 1
```

until the team has an explicit replacement design that maps legacy profiles, access patterns, roles, and privileged users outside Oracle.

## Spring/JPA Implementation Guidance

Do not set `FLAG_PACK` in a standalone connection before calling a Spring Data repository. The repository query may use a different pooled connection.

Preferred shapes:

- Wrap the service method in one transaction.
- Set context immediately before the repository/native query inside that transaction.
- Use the current transactional connection, for example through `EntityManager.unwrap(Session.class).doWork(...)`, `JdbcTemplate` participating in the same transaction, or another established local helper that uses `DataSourceUtils`.
- Overwrite all relevant package variables for every request before executing the query.
- Clear or overwrite context before the transaction completes if the same pooled connection may be reused by unrelated work.

If the app uses repository `@Query(nativeQuery = true)` methods, add a service-layer context initializer around those repository calls rather than embedding context setup in every repository method.

## Cleanup Guidance

Connection pooling makes stale package state a real risk. The minimum rule is:

- Never assume package state starts empty.
- Set every required context value on every scoped operation.
- Prefer a `finally` cleanup that clears `usuario`, `transacao`, and `empresa` or calls an agreed Oracle reset routine if available.
- Add a test that executes two requests with different users/companies on a reused connection and proves the second result is not contaminated by the first.

## When To Replace Oracle Context

Replacing `FLAG_PACK` with explicit Java authorization is a separate migration decision. Only do this when the team has mapped:

- legacy user to API principal;
- `USUARIO.PRIVIL`;
- HADES access patterns and roles;
- screen transaction access;
- company scope;
- type/code frequency profiles;
- write permission letters such as `C`, `A`, and `R`.

Until then, mark the screen as `Ready for read API` only if the Java context-setting strategy is implemented or explicitly accepted as a prerequisite for implementation.
