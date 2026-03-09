# picoCTF: Web Exploitation Challenge Writeup

## Challenge Description
Proper session timeout controls are critical for securing user accounts. If a user logs in on a public or shared computer but doesn’t explicitly log out (instead simply closing the browser tab), and session expiration dates are misconfigured, the session may remain active indefinitely.
This then allows an attacker using the same browser later to access the user’s account without needing credentials, exploiting the fact that sessions never expire and remain authenticated.

**Hints:**
- Do you know how to use the web inspector?
- Where are cookies stored?

**Target URL:** `http://dolphin-cove.picoctf.net:54123/login`

## Solution Steps

1. **Initial Access and Reconnaissance**
   Accessing the target URL `http://dolphin-cove.picoctf.net:54123/login` presents a login page. There is also a link to register a new account at `/register`.

2. **Account Registration and Login**
   Since we don't have valid credentials, the first step is to create an account. By submitting a `POST` request to `/register` with details (e.g., `username=jules`, `password=test123`, `conf_password=test123`), an account is successfully created, and the server redirects to the login page.
   Subsequently, logging in via `/login` redirects to the homepage `/` and sets a `session` cookie.

3. **Exploring the Application**
   Looking at the homepage at `/`, there are some comments from users. One interesting comment from `mary_jones_8992` says: "Hey I found a strange page at `/sessions`".

4. **Investigating the `/sessions` Endpoint**
   Navigating to `http://dolphin-cove.picoctf.net:54123/sessions` reveals a list of active sessions stored by the application:
   ```html
   <p>1) session:BM_sFZ8vmumCSqncuFcfzyTlPOj4U933Vs-Lgzt01dk, {'_permanent': True, 'key': 'admin'}</p>
   <p>2) session:SdUXqHD5-rneAy85smfJzATCcksgj1n67eAHJDKMhuw, {'_permanent': True, '_flashes': [['error', None]]}</p>
   <p>3) session:KwgFsoHNuj02unngRVf7m2dMfjRgqkMdq_BZ-TBbJ0c, {'_permanent': True, '_flashes': [['error', None]]}</p>
   <p>4) session:_GibmvGuqoIo4e_AeHBhUmAL3IdrA_G7KSmT9fasgJk, {'_permanent': True, 'key': 'jules'}</p>
   ```

5. **Session Hijacking**
   The `/sessions` page exposes valid session tokens, including one for the `admin` user (`BM_sFZ8vmumCSqncuFcfzyTlPOj4U933Vs-Lgzt01dk`).
   Because the challenge description mentioned that "sessions never expire and remain authenticated," we can hijack the admin's session.

6. **Retrieving the Flag**
   By setting our browser's `session` cookie to the admin's session value (`BM_sFZ8vmumCSqncuFcfzyTlPOj4U933Vs-Lgzt01dk`) and accessing the homepage `/`, we bypass authentication and log in as the `admin` user.
   ```bash
   curl -v -b "session=BM_sFZ8vmumCSqncuFcfzyTlPOj4U933Vs-Lgzt01dk" http://dolphin-cove.picoctf.net:54123/
   ```

   The homepage for the admin user contains the flag:
   `<p class="flag-message">picoCTF{s3t_s3ss10n_3xp1rat10n5_7139c037}</p>`

## Flag
`picoCTF{s3t_s3ss10n_3xp1rat10n5_7139c037}`