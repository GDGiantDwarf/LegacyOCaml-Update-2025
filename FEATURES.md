# Feature

## Options

| Feature              | Description                          |
|----------------------|--------------------------------------|
| -a <ADDRESS>         | Select a specific address (default = any address of this computer).  |
| -add_lexicon <FILE>  | Add file as lexicon.        |
| -allowed_tags <FILE> | HTML tags which are allowed to be displayed. One tag per line in file.      |
| -auth <FILE>         | Authorization file to restrict access. The file must hold lines of the form "user:password".                |
| -bd <DIR>            | Specify where the “bases” directory with databases is installed (default if empty is “bases”).        |
|  -blang              | Select the user browser language if any.        |
| -cache-in-memory <DATABASE>  | Preload this database in memory        |
| -cache_langs         | Lexicon languages to be cached.        |
| -cgi                 | Force CGI mode.        |
| -cgi_secret_salt <STRING>  | Add a secret salt to form digests.        |
| -conn_tmout <SEC>    | Connection timeout (only on Unix) (default 120s; 0 means no limit).        |
| -daemon              | Unix daemon mode.        |
| -debugon             | Enable debug mode        |
| -digest              | Use Digest authorization scheme (more secure on passwords)        |
| -etc_prefix <DIR>    | Specify where the “etc” directory is installed (default if empty is [-hd value]/etc).        |
| -friend <PASSWD>     | Set a friend password.        |
| -hd <DIR>            | Specify where the “etc”, “images” and “lang” directories are installed (default if empty is “gw”).        |
| -images_dir <DIR>    | Same than previous but directory name relative to current.        |
| -images_prefix <DIR> | Specify where the “images” directory is installed (default if empty is [-hd value]/images).        |
| -lang <LANG>         | Set a default language (default: fr).        |
| -log <FILE>          | Log trace to this file. Use "-" or "<stdout>" to redirect output to stdout or "<stderr>" to output log to stderr.        |
| -log_level <N>       | Send messages with severity <= <N> to syslog (default: 6).        |
| -login_tmout <SEC>   | Login timeout for entries with passwords in CGI mode (default 1800s).        |
| -max_clients <NUM>   | Max number of clients treated at the same time (default: no limit) (not cgi) (DEPRECATED).        |
| -max_pending_requests <NUM>  | Maximum number of pending requests (default: 150)        |
| -min_disp_req        | Minimum number of requests in robot trace (default: 6).        |
| -n_workers <NUM>     | Number of workers used by the server (default: 20)        |
| -no-fork             | Prevent forking processes (DEPRECATED)        |
| -no_host_address     | Force no reverse host by address.        |
| -nolock              | Do not lock files before writing.        |
| -only <ADDRESS>      | Only inet address accepted.        |
| -p <NUMBER>          | Select a port number (default = 2317).        |
| -plugin <PLUGIN>.cmxs| load a safe plugin. Combine with -force to enable for every base. Combine with -unsafe to allow unverified plugins. e.g. "-plugin -unsafe -force".        |
| -plugins <DIR>       | load all plugins in <DIR>. Combine with -force to enable for every base. Combine with -unsafe to allow unverified plugins. e.g. "-plugins -unsafe -force".        |
| -predictable_mode    | Turn on the predictable mode. In this mode, the behavior of the server is predictable, which is helpful for debugging or testing. (default: false)        |
| -redirect <ADDR>     | Send a message to say that this service has been redirected to <ADDR>.        |
| -robot_xcl <CNT>,<SEC>  | Exclude connections when more than <CNT> requests in <SEC> seconds.        |
| -setup_link          | Display a link to local gwsetup in bottom of pages.        |
| -trace_failed_passwd | Print the failed passwords in log (except if option -digest is set).        |
| -version             | Print the Geneweb version, the source repository and last commit id and message.        |
| -wd <DIR>            | Directory for socket communication (Windows) and access count.        |
| -wizard <PASSWD>     | Set a wizard password.        |
| -wjf                 | Wizard just friend (permanently).        |
| -help                | Display this list of options        |
| --help               | Display this list of options        |


## Interfaces


### Handle Bases

| Feature              | Description                          |
|----------------------|--------------------------------------|
| Saisir une chronique         | adddd  |
| Requete évoluée         | adddd  |
| Calendrier         | adddd  |
| Configuration         | adddd  |
| Ajouter note         | adddd  |
| Ajouter famille         | adddd  |


### Management and creation

| Feature              | Description                          | Options                           |
|----------------------|--------------------------------------|-----------------------------------|
| Consult - family Trees (Bases)          | Page with all databases created and link to each of them | - |
| Consult - error history and statistics  | Page who display the content of comm.log and the content of gwsetup.log | - |
| Save - GEDCOM source file               | Page where you can Extract a GEDCOM file from a bases created - Add all options  | -Select your database\ -name you want to give to your GEDCOM file\ -charset: ASCII/UTF-8/ANSEL/ANSI (I-SO 8859-1)\ -mem: Save the memory space during the operation (but it will be slower)\ -nn: Do not extract notes\ -nopicture: Dont extract individual pictures (portraits)\ -picture-path: Extract individual pictures path (portraits)\ -Extract only the ancestors: first name/num/surname\ -Extract only the descendants: first name/num/surname\ -Extract ancestors with siblings: first name/num/surname\ -Extract surname: surname\ -c: When a person is born less than years ago, it is not exported unless it is Public\All the spouses and descendants are also censored\ -nsp: Do not extract spouses' parents (for options -s and -d) |

| Save - GeneWeb source file              | Page where you can Extract a GeneWeb file from a bases created - add all options  |
        -name you want to give to your GeneWeb source file,
        -Save isolated persons,
        -Save all files in notes_d, including those without Wiki links,
        -Save memory space during operation (but it will be slower),
        -Extract only the ancestors: first name/num/surname,
        -Extract only the descendants: first name/num/surname |
| Import - GEDCOM source file             | Page where you can create a bases from a GEDCOM file with option -  add all option  |
        -select GEDCOM file,
        -name of the folder holding databases,
        -name of your GeneWeb databases you want,
        -Delete database if already existing,
        -Put untreated GEDCOM tags in notes,
        -Convert first names to lowercase letters, with initials in uppercase,
        -Convert surnames to lowercase letters, with initials in uppercase. Try to keep lowercase particles
        -When creating a person, if the GEDCOM first name part holds several names separated by spaces, you can ask that the first of this names becomes the person "first name" and the complete GEDCOM first name part a "first name alias" (-no_efn default),
        -"first names enclosed": the -fne option must be followed by a two characters string "be". When creating a person, if the GEDCOM first name part holds a part between 'b' (any character) and 'e' (any character), it is considered to be the usual first name: e.g. -fne "\\" or -fne "()",
        -By default, when creating a person, if the GEDCOM first name part looks like a public name, i.e. holds:
        A number or a roman number, supposed to be a number of a nobility title (e.g. George V)
        One of the words: "der", "den", "die", "el", "le", "la", "the", supposed to be the beginning of a qualifier (e.g. William the Conqueror)
        then the GEDCOM first name part becomes the person "public name" and its first word his "first name" (-epn default),
        -Not public even if titles (see -epn option),
        -Set negative dates when inconsistency (e.g. birth after death),
        -No negative dates: do not interpret a year preceded by a minus sign as a negative year,
        -No consistency check,
        -Don't extract individual picture,
        -Force relation status to "NoMention" (default is "Married"),
        -Reorg mode
        -Default source,
        -Some GEDCOM files sometimes write dates with numbered months (from 1 to 12). The GEDCOM standard 5.5 requires that the months be represented by identifiers (e.g. "MAY 1912" and not "05/1912"). The notation "02/05/1912" is ambiguous (means "May 2, 1912" or "February 5, 1912" according to the countries),
        -The accentuated characters encoding is normally specified in the GEDCOM header |
| Import - GeneWeb source file            | Page where you can create a bases from a GeneWeb file with option -  add all option | 
        -selected source file/file name(relative to the path), 
        -name of the folder holding databases,
        -name of your GenWeb databases you want,
        -Display some statistics at the end (they will be visible in the traces),
        -Do not check the consistency of the data,
        -End by the initialization of consanguinities,
        -Delete database if already existing,
        -Kill .gwo files after base creation,
        -Reorg mode |
| Import - an empty file                  | Page where you can create a bases from nothings | -name, -Reorg mode |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |
| qdddd         | adddd  |


