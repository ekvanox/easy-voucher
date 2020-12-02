# Easy Voucher - Account duplicate detection bypass

## UberEats
### Identification methods
* Credit card info
* Browser/Device fingerprinting
* Phone number
* Email address

### Bypass methods
1. **Credit card info**
    Pay with paypal instead.   
    The paypal account can be connected to the original credit card (even if it has been blacklisted) because paypal does not appear to forward personally identifyable information to UberEats. Hence it cannot be blocked in the same way.
    
    You can change your email address freely in paypal, which I recommend you do as UberEats might use that information for identifying duplicate accounts.
2. **Browser/Device fingerprinting**
    The fingerprint can be changed through browser extensions, like [CyDec Platform Anti-Fingerprinting](https://www.cydecplatform.com/antifp.html). I don't believe the client IP-address is included in the fingerprint, although I'm not sure.
3. **Phone number**
    Sim cards can picked up for free from [Lycamobile](https://www.lycamobile.com/) providing stores. Alternatively you can use temporary numbers from VoIP providing sites like [Twilio](https://www.twilio.com/) to recieve SMS.
4. **Email address**
    #### Temporary email
    Temporary emails are provided by many sites, like [Temp Mail](https://temp-mail.org) or [Vedbex](https://www.vedbex.com/tools/tempmail)
    #### Your own email
    If you have a gmail account `example@gmail.com` you can trick UberEats by inserting dots into the email username like so:   
    `e.x.am.ple@gmail.com`
    
    You can also change gmail.com to googlemail.com like so:
    `example@googlemail.com`
    
    
    Or replacing lowercase letters with uppercase letters:
    `eXaMpLe@gmail.com`
    
    These can all be combined and will be resolved to your original email address in the end.
    #### Create your own email domain
    Domains can be registered for free with [Freenom](https://www.freenom.com/en/index.html?lang=en), DNS records can be configured with [Cloudflare](https://dash.cloudflare.com/login) and catch-all email forwarding can be hosted with [ImprovMX](https://app.improvmx.com/).
    
    If you registered example.ml you would recieve all the emails to your real account:
    `username@example.ml`
    `1@example.ml`
    `info@example.ml`
    `aaaaaaaaaaaaaaaa@example.ml`
    #### Random email account
    You can also enter an email account that you don't even own, as your email address never has to be verified for you to make your order. This is quite handy for mass account creation.
    
    By setting the `emailAddress` flag to `true` in the configuration file, this is done automatically by the script.
    
## Foodora