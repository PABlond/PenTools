### bruteforce_login_POST_basic/

Given the following form:

    <form action="http://localhost/login" method="POST">
        <input type="text" name="user" />
        <input type="password" name="pass" />
        <button type="submit">LOGIN</button>
    </form>

You can use the script in "bruteforce_login_POST_basic" folder as follows:

    python run.py  -f /path/to/wordlist.txt -U http://localhost/login -p R4nd0m? -uu user -up pass 