# Credidentials
This repository holds templates and encrypted credentials used by ElectronPass as well as `configure.py` script for compiling the templates.

## Dependencies
- [openssl](https://www.openssl.org/)


## Why and how?
When using  APIs provided by online services such as Google Drive, Mega, Dropbox, programs usually have to identify themselves using a ID and SECRET. As the name suggests, at least SECRET has to be kept secret. Publishing it in the source code therefore is not an option. For retrieving your own credentials, refer to [RETRIEVING_CREDENTIALS.](https://github.com/electronpass/credentials/blob/master/RETRIEVING_CREDENTIALS.md)

Each app (desktop, Android, iOS ...) uses a special configuration file which provides those variables to the compiler. Compiler then embeds them into binaries in the compile time. Why compile time? Well, if there were a configuration file containing all those variables embedded in each package, it would be quite an easy job to find it. Making it part of the binary makes it at least a bit harder, but avoiding embedding this info into our program completely is unfortunately not possible. If you somehow manage to retrieve this information from binaries, please tell us how, so we can improve ElectronPass (possibly using some obfuscation techniques).

Template configuration files for each platform is saved as `[platform_name].tpl` (`desktop.tpl` for example). Templates also support comments, for example refer to [`desktop.template`](https://github.com/electronpass/credentials/blob/master/desktop.tpl) Template gets compiled into final configuration file using `configure.py` like this:

    python3 configure.py [file_to_decrypt] [encryption_pass] [template_to_compile] [output_file]

`sample.json` is a file providing sample keys. To set it as input file in configure.py you have to encrypt it first. Decrypt and encrypt files using openssl like this:
- encryption: `openssl aes-256-cbc -a -in [file_to_encrypt] -out [output_file]`
- decryption: `openssl aes-256-cbc -a -d -in [file_to_decrypt] -out [output_file]`

BEWARE: `keys.json` file will be overridden and deleted by `configure.py` in compilation process. (Why decrypt content to file and then read it? 1.: We can use exact same commands as in terminal. 2.: no need to pipe output. 3.: easier to check command output)

#### Build procedure
Currently, all of our apps are built using [Travis CI](https://travis-ci.org/). Such Travis configuration for desktop app is available [here](https://github.com/electronpass/electronpass-desktop/blob/master/.travis.yml). To put it simple, Travis downloads and builds all the dependencies. Then it clones this repository and runs `configure.py`, specifying the password set in a Travis control panel (so only Travis and project admins know it). `configure.py` replaces the sample keys file in project sources with the right one and builds the app.

## Advantages and drawbacks
#### Advantages:
- all of the code is open source, except for the keys which can't be,
- builds can easily be automated,
- anyone can fill in his personal keys and deploy any app without having to touch the code,
- all keys are kept in one place, which makes it easy to add new keys or edit the old ones.

#### Drawbacks:
- this approach is quite complex and might seem like using a cannon to kill flies and
- it involves publishing encrypted content into public GitHub repositories which might be problematic? (I didn't find any good related article.)

## Further development
Encryption in this repository could be done using [git-crypt](https://github.com/AGWA/git-crypt) to make it easier for users and developers to use it.

Binaries containing the secret information could be processed using some obfuscation techniques to make retrieving this data harder.

## License
Code in this project is licensed under [GNU GPLv3 license](https://github.com/electronpass/credentials/blob/master/LICENSE).
