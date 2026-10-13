# Dangerous sinks and safe replacements

Open this to check the language in front of you. A sink is only a finding if untrusted data can reach it.

## Python

| Sink | Risk | Safe replacement |
|---|---|---|
| `cursor.execute(f"...{x}...")`, `%` or `+` building SQL | SQL injection | `execute("... ?", (x,))` or ORM parameters |
| `os.system`, `subprocess.*(..., shell=True)` | Command injection | `subprocess.run([...], shell=False)` with an argument list |
| `eval`, `exec`, `compile` | Code execution | `ast.literal_eval` for literals, or don't |
| `pickle.loads`, `yaml.load` (non-safe loader), `marshal` | Deserialization RCE | `json`, `yaml.safe_load` |
| `open(base + user_path)`, `send_file(user_path)` | Path traversal | Resolve with `os.path.realpath` and check it stays under the base directory |
| `requests.get(user_url)` | SSRF | Allow-list hosts, block private and metadata IP ranges after DNS resolution |
| `render_template_string(user_input)`, `Template(user_input)` | Template injection | Render fixed templates with user data as variables |
| `random.*` for tokens | Predictable secrets | `secrets.token_urlsafe` |

## JavaScript / TypeScript (Node)

| Sink | Risk | Safe replacement |
|---|---|---|
| Template strings in `db.query(...)` | SQL injection | Parameterized queries (`$1`, `?`) |
| `child_process.exec(cmd)` | Command injection | `execFile` / `spawn` with an argument array |
| `eval`, `new Function`, `vm.runInNewContext` | Code execution | Avoid. `vm` is not a sandbox |
| `res.sendFile(userPath)`, `path.join(base, user)` | Path traversal | `path.resolve`, then check the prefix; `root` option on `sendFile` |
| `Object.assign(target, userObj)`, deep merge of user JSON | Prototype pollution | Reject `__proto__`, `constructor`, `prototype` keys; use `Object.create(null)` |
| `fetch(userUrl)` | SSRF | Host allow-list, block private ranges |
| `innerHTML`, `dangerouslySetInnerHTML`, `document.write` | XSS | `textContent`, framework escaping, a sanitizer like DOMPurify |
| `jwt.decode` without `verify` | Auth bypass | `jwt.verify` with pinned algorithms |
| `Math.random` for tokens | Predictable secrets | `crypto.randomBytes`, `crypto.randomUUID` |

## Go

| Sink | Risk | Safe replacement |
|---|---|---|
| `db.Query(fmt.Sprintf(...))` | SQL injection | `db.Query("... $1", x)` |
| `exec.Command("sh", "-c", s)` | Command injection | `exec.Command(bin, args...)` without a shell |
| `filepath.Join(base, user)` | Path traversal | `filepath.Clean`, then check the prefix; Go 1.24+ `os.Root` |
| `text/template` for HTML | XSS | `html/template` |
| `http.Get(userURL)` | SSRF | Custom dialer that rejects private IPs |
| `math/rand` for tokens | Predictable secrets | `crypto/rand` |

## Java

| Sink | Risk | Safe replacement |
|---|---|---|
| `Statement.execute("..." + x)` | SQL injection | `PreparedStatement` with `?` |
| `Runtime.exec(String)` | Command injection | `ProcessBuilder` with an argument list |
| `ObjectInputStream.readObject` on untrusted data | Deserialization RCE | JSON, or an `ObjectInputFilter` allow-list |
| XML parsers with default settings | XXE | Disable DTDs and external entities |
| `new File(base, user)` | Path traversal | `toRealPath()`, then check `startsWith(base)` |
| `java.util.Random` for tokens | Predictable secrets | `SecureRandom` |

## Any language

- Logging untrusted input without encoding: log injection, and secrets in logs.
- Redirecting to a user-supplied URL: open redirect.
- Regex on untrusted input with nested quantifiers: ReDoS.
- Comparing secrets with `==`: timing side channel.
