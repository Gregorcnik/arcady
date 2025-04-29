# Arcady

A project featuring a set of arcade-inspired games with an integrated game selection menu. Developed as part of the programming club at Gimnazija Vič.

## How to run

### Prerequisites

- **git**: You can download it from its official [website](https://git-scm.com/)
  or using your preferred package manager.
- **python 3.9+**: You can download it from its official
  [website](https://www.python.org/downloads/) or using your preferred package
  manager.

When running stuff on Windows install [git-bash](https://gitforwindows.org/) for
a somewhat proper commandline interface and working python.

In order to run the game for the first time follow steps bellow:

0. **Set up ssh keys**: The guide to set up ssh keys is in the subsection below
   installation subsection.

1. **Clone the repository**:
    ```bash
    git clone git@github.com:schrjako/arcady.git
    cd arcady
    ```

2. **Create virtual enviroment**: Virtual enviroment is useful for keeping
  installed libraries separated. Create it with
    ```bash
    {python path} -m venv ./venv
    ```
    and than activate it with
    ```bash
    source venv/bin/activate        #   on linux
    source venv/Scripts/activate    #   on Windows
    ```

3. **Download the necessary libraries**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run main.py**:
    ```bash
    python main.py
    ```

If the shell doesn't find python you can try to find it with:
    ```bash
    which python
    ```

After the first time when setting up the clone and environment, you just have to
**activate virtual enviroment** again (`source venv/bin/activate`), install
aditional requirements (`pip install -r requirements.txt` if `requirements.txt`
changed) and you're good to go (you can **run main.py**: `python main.py`).

## Setting up ssh keys

For a more in-depth explanation you can read github's [documentation on ssh key
generation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent),
but the guide below should be enough.

If  you're working on a new computer, you'll have to generate and add new ssh
keys for that machine. To check whether you already have ssh keys run
    ```bash
    ls ~/.ssh
    ```
If this command prints `id_X`, `id_X.pub` (possibly among other fillenames; `X`
here is a string of letters and or digits), you already have an ssh key on this
machine and can skip the generating step.

### Generate an ssh key

To generate a new ssh key, run:
    ```bash
    ssh-keygen
    ```

The program asks you for the destination of the key, which you can leave to be
the default value. Afterwards you're asked for a passphrase, which you'll have
to type in every time you use the key (when pushing/pulling from github) which
you can leave empty. The password is not echoed (which means there is no
indication that the program has read what you typed, but it *has*).

### Adding your ssh key to github

When you have your ssh key, you can add it to your github account. The public
part of the key (which you want to share with github) is stored under
`~/.ssh/id_X.pub`. You can copy it to your clipboard by opening it in a text
editor, or by running `cat ~/.ssh/id_X.pub | xclip -i -selection clipboard` on
Linux, `cat ~/.ssh/id_X.pub | clip` on Windows, and `cat ~/.ssh/id_X.pub |
pbcopy` on Mac.

You can now add the public part of your key to your account in the account
settings (top right icon -> *settings*) -> *SSH and GPG keys* -> *New SSH key*.
Under title type in some name for the key, by which you will know for which
computer this key is relevant.

When you have your key added to your github account you can pull/push things
from/to github without typing in your password (and much more safely as well).
