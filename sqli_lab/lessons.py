LESSONS = [
    {
        "slug": "error-based",
        "title": "Error-based SQL injection",
        "summary": "Database errors reveal query structure and data.",
        "body": """
<p>When user input is concatenated into SQL, malformed payloads can trigger verbose errors that leak table or column names.</p>
<pre class="code">SELECT flag FROM secrets WHERE id = 'USER_INPUT'</pre>
<p><strong>Example placeholder:</strong> <code>' OR 1=1 --</code></p>
<h3>What defenders do</h3>
<ul>
<li>Use parameterized queries / prepared statements.</li>
<li>Return generic errors to clients; log details server-side only.</li>
<li>Disable verbose SQL errors in production.</li>
</ul>
""",
        "quiz": {
            "question": "What is the primary fix for error-based SQLi?",
            "options": ["Hide the login button", "Parameterized queries", "Use HTTP POST only", "Add CAPTCHA"],
            "answer": 1,
        },
    },
    {
        "slug": "union-based",
        "title": "UNION-based SQL injection",
        "summary": "Append UNION SELECT to pull columns from other tables.",
        "body": """
<p>UNION attacks require matching column count and compatible types. Attackers probe with <code>ORDER BY</code> or <code>UNION SELECT NULL,NULL</code>.</p>
<pre class="code">' UNION SELECT 1, name, flag, 4 FROM lab_products --</pre>
<h3>What defenders do</h3>
<ul>
<li>Parameterized queries; allow-lists for sortable columns.</li>
<li>Principle of least privilege on DB accounts.</li>
</ul>
""",
        "quiz": {
            "question": "UNION attacks need:",
            "options": ["Matching column count", "Admin cookies", "HTTPS disabled", "A WAF only"],
            "answer": 0,
        },
    },
    {
        "slug": "boolean-blind",
        "title": "Boolean-based blind SQLi",
        "summary": "Infer data from true/false application responses.",
        "body": """
<p>No data is returned directly; the app behaves differently when a subquery is true vs false.</p>
<pre class="code">' AND (SELECT substr(bio,1,1) FROM lab_profiles WHERE username='bob')='F' --</pre>
<h3>What defenders do</h3>
<ul>
<li>Parameterized queries; consistent response times and messages.</li>
<li>Monitoring for repetitive probing patterns.</li>
</ul>
""",
        "quiz": {
            "question": "Boolean blind SQLi relies on:",
            "options": ["Visible stack traces", "Different app behavior for true/false", "Email exfiltration", "DNS only"],
            "answer": 1,
        },
    },
    {
        "slug": "time-based",
        "title": "Time-based blind SQLi",
        "summary": "Infer truth from measurable delays.",
        "body": """
<p>When no visible difference exists, heavy queries or DB sleep functions introduce delays for true conditions.</p>
<h3>What defenders do</h3>
<ul>
<li>Query timeouts; ORMs; rate limiting.</li>
<li>WAF / RASP can help but are not a substitute for secure code.</li>
</ul>
""",
        "quiz": {
            "question": "Time-based blind SQLi measures:",
            "options": ["Response delay", "JPEG size", "Cookie length", "CSS color"],
            "answer": 0,
        },
    },
    {
        "slug": "auth-bypass",
        "title": "Authentication bypass",
        "summary": "Break login queries without valid credentials.",
        "body": """
<pre class="code">admin' --</pre>
<p>Classic login query: <code>WHERE user='...' AND pass='...'</code></p>
<h3>What defenders do</h3>
<ul>
<li>Never build auth SQL with string concatenation.</li>
<li>MFA, account lockout, and secure session cookies.</li>
</ul>
""",
        "quiz": {
            "question": "Auth bypass targets:",
            "options": ["Login SQL logic", "Favicon cache", "CDN headers", "robots.txt"],
            "answer": 0,
        },
    },
    {
        "slug": "second-order",
        "title": "Second-order SQLi",
        "summary": "Payload is stored safely first, executed unsafely later.",
        "body": """
<p>Registration or comment storage may use prepared statements, but a later report feature may concatenate stored values.</p>
<h3>What defenders do</h3>
<ul>
<li>Parameterize every query, including those using stored data.</li>
<li>Treat stored user content as untrusted at read time.</li>
</ul>
""",
        "quiz": {
            "question": "Second-order SQLi happens when:",
            "options": [
                "Payload runs immediately in the same query",
                "Stored input is used unsafely in a later query",
                "Only NoSQL is used",
                "TLS is expired",
            ],
            "answer": 1,
        },
    },
    {
        "slug": "stacked-queries",
        "title": "Stacked queries",
        "summary": "Multiple statements in one execution (advanced).",
        "body": """
<p>Some drivers allow <code>;</code> separated statements. This lab gates stacked demos behind advanced mode and provides a reset script.</p>
<h3>What defenders do</h3>
<ul>
<li>Disable multi-statement execution where possible.</li>
<li>Least-privilege DB roles (no DDL for app users).</li>
</ul>
""",
        "quiz": {
            "question": "Stacked queries require:",
            "options": ["Multi-statement execution support", "GraphQL", "IPv6", "WebSockets"],
            "answer": 0,
        },
    },
    {
        "slug": "out-of-band",
        "title": "Out-of-band SQLi (concept)",
        "summary": "Exfiltration via DNS/HTTP to attacker-controlled servers.",
        "body": """
<p>OOB techniques use database features (e.g. <code>xp_dirtree</code>, <code>UTL_HTTP</code>) to call external hosts. This lab covers the concept only — no live OOB channel.</p>
<h3>What defenders do</h3>
<ul>
<li>Network egress filtering from database servers.</li>
<li>Parameterized queries and minimal DB privileges.</li>
</ul>
""",
        "quiz": {
            "question": "Out-of-band SQLi typically exfiltrates via:",
            "options": ["External network callbacks", "Browser fonts", "LocalStorage", "CSS grid"],
            "answer": 0,
        },
    },
    {
        "slug": "mitigations",
        "title": "Defense in depth",
        "summary": "Parameterization, ORMs, least privilege, WAF basics.",
        "body": """
<ul>
<li><strong>Parameterized queries</strong> — separate code from data.</li>
<li><strong>ORMs</strong> — safe defaults; still avoid raw unsafe queries.</li>
<li><strong>Least privilege</strong> — app DB user cannot DROP or alter schema.</li>
<li><strong>WAF</strong> — helpful layer, not a replacement for secure development.</li>
</ul>
""",
        "quiz": {
            "question": "The most important SQLi fix is:",
            "options": ["WAF only", "Parameterized queries", "Changing port 443", "Removing forms"],
            "answer": 1,
        },
    },
]


def get_lesson(slug: str):
    for lesson in LESSONS:
        if lesson["slug"] == slug:
            return lesson
    return None
