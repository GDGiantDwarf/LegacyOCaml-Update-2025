# Features

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

### Genweb

| Feature               | Description                          |
|-----------------------|--------------------------------------|
| button to Family Tree | button link to Family Tree (gwd)     |
| button to Management and creation | button link to Management and creation (gwsetup)     |
| button to User guide | button link to user guide: http://geneweb.tuxfamily.org/wiki/GeneWeb   |
| button to README.txt | button link to README.txt: readme file in distrib     |
| button to License | button link to License: https://github.com/geneweb/geneweb/blob/master/LICENSE     |
| Update Language | available langauge: Deutsch, English, Español, Français, Italiano, Latvian, Nederlands, Norsk, Suomi, Svenska     |


### Handle Bases

| Feature              | Description                          | Options                           |
|----------------------|--------------------------------------|-----------------------------------|
| add notes         | write a note | -text area  |
| Advanced request         | page where you can start an advanced request  | -Search type: AND/OR<br>-Individual Sex: M-F<br>-First name<br>-Surname<br>-Occupations<br>-Birth: Place, after(monht, day, year), before(month, day, year)<br>-Death: Died, alive, maybe alive.Place, after(month, day, year), before(month, day, year)<br>-Marriage(yes, no): Place, after(month, day, year), before(month, day, year)<br>-Baptism: Place, after(month, day, year), before(month, day, year)<br>-Burial: Place, after(month, day, year), before(month, day, year)<br>-Maximum individuals |
| Calendars         | Page where you can change the month, day and year for Gregorian, Julian, French republican and Hebrew calendars | -Month, day, year |
| Configuration         | page where you can watch all the base's configuration | -GeneWeb version<br>-User<br>-Username<br>-userkey<br>-lang<br>-lang fallback<br>-default_lang<br>-browser_lang<br>Launch arguments of Gwd server: <br>-Mode<br>-prefix<br>-etc_prefix<br>-images_prefix<br>Configuration parameters:<br>-Mode<br>-access_by_key<br>-disable_forum<br>-hide_private_names<br>-use_restrict<br>-show_consang<br>-display_sosa<br>-place_surname_link_to_ind<br>-max_anc_level<br>-max_anc_tree<br>-max_desc_level<br>-max_desc_tree<br>-max_cousins<br>-max_cousins_level<br>-latest_event<br>-template<br>-long_date<br>-counter<br>-full_siblings<br>-hide_advanced_request<br>-p_mod  |
| add note         | page where you can create a new note  | -name of the new note |
| add family         | page where you can add a family(parents, events, children, sources, comment) | Parents:<br>-First name (M)<br>-Surname<br>-Birth(month, day, year, place)<br>-Death(month, day, year, place)<br>-Occupation<br>-First name (F)<br>-Surname<br>-Birth(month, day, year, place)<br>-Death(month, day, year, place)<br>-Occupation<br>-Same sex couple<br>Events:<br>-select an event in a list<br>-Place<br>-Date(month, day, year, place)<br>-Notes<br>-Sources<br>-add n witness<br>-add n new events<br>Children:<br>-add n new children<br>-create new child or link on<br>-first name<br>-Surname<br>-sex(M of F)<br>-Birth(month, day, year, place)<br>-Death(month, day, year, place)<br>-Occupation<br>Sources:<br>-Individuals<br>-Family<br>Comment(text area) |


### Management and creation

| Feature              | Description                          | Options                           |
|----------------------|--------------------------------------|-----------------------------------|
| Consult - family Trees (Bases)          | Page with all databases created and link to each of them | - |
| Consult - error history and statistics  | Page who display the content of comm.log and the content of gwsetup.log | - |
| Save - GEDCOM source file               | Page where you can Extract a GEDCOM file from a bases created | -Select your database<br> -name you want to give to your GEDCOM file<br> -charset: ASCII/UTF-8/ANSEL/ANSI (I-SO 8859-1)<br> -mem: Save the memory space during the operation (but it will be slower)<br> -nn: Do not extract notes<br> -nopicture: Dont extract individual pictures (portraits)<br> -picture-path: Extract individual pictures path (portraits)<br> -Extract only the ancestors: first name/num/surname<br> -Extract only the descendants: first name/num/surname<br> -Extract ancestors with siblings: first name/num/surname<br> -Extract surname: surname<br> -c: When a person is born less than years ago, it is not exported unless it is Public<br>All the spouses and descendants are also censored<br> -nsp: Do not extract spouses' parents (for options -s and -d) |
| Save - GeneWeb source file              | Page where you can Extract a GeneWeb file from a bases created | -name you want to give to your GeneWeb source file<br>-Save isolated persons<br>-Save all files in notes_d, including those without Wiki links<br>-Save memory space during operation (but it will be slower)<br>-Extract only the ancestors: first name/num/surname<br>-Extract only the descendants: first name/num/surname |
| Import - GEDCOM source file             | Page where you can create a bases from a GEDCOM file with option | -select GEDCOM file<br>-name of the folder holding databases<br>-name of your GeneWeb databases you want<br>-Delete database if already existing<br>-Put untreated GEDCOM tags in notes<br>-Convert first names to lowercase letters, with initials in uppercase<br>-Convert surnames to lowercase letters, with initials in uppercase. Try to keep lowercase particles<br>-When creating a person, if the GEDCOM first name part holds several names separated by spaces, you can ask that the first of this names becomes the person "first name" and the complete GEDCOM first name part a "first name alias" (-no_efn default)<br>-"first names enclosed": the -fne option must be followed by a two characters string "be". When creating a person, if the GEDCOM first name part holds a part between 'b' (any character) and 'e' (any character), it is considered to be the usual first name: e.g. -fne "\\" or -fne "()"<br>-By default, when creating a person, if the GEDCOM first name part looks like a public name, i.e. holds:A number or a roman number, supposed to be a number of a nobility title (e.g. George V) One of the words: "der", "den", "die", "el", "le", "la", "the", supposed to be the beginning of a qualifier (e.g. William the Conqueror) then the GEDCOM first name part becomes the person "public name" and its first word his "first name" (-epn default)<br>-Not public even if titles (see -epn option)<br>-Set negative dates when inconsistency (e.g. birth after death)<br>-No negative dates: do not interpret a year preceded by a minus sign as a negative year<br>-No consistency check<br>-Don't extract individual picture<br>-Force relation status to "NoMention" (default is "Married")<br>-Reorg mode<br>-Default source<br>-Some GEDCOM files sometimes write dates with numbered months (from 1 to 12). The GEDCOM standard 5.5 requires that the months be represented by identifiers (e.g. "MAY 1912" and not "05/1912"). The notation "02/05/1912" is ambiguous (means "May 2, 1912" or "February 5, 1912" according to the countries)<br>-The accentuated characters encoding is normally specified in the GEDCOM header |
| Import - GeneWeb source file            | Page where you can create a bases from a GeneWeb file with option | -selected source file/file name(relative to the path)<br>-name of the folder holding databases<br>-name of your GenWeb databases you want<br>-Display some statistics at the end (they will be visible in the traces)<br>-Do not check the consistency of the data<br>-End by the initialization of consanguinities<br>-Delete database if already existing<br>-Kill .gwo files after base creation<br>-Reorg mode |
| Import - an empty file                  | Page where you can create a bases from nothings | -name<br>-Reorg mode |
| Update language used                    | can change the default language from the menu |-Corsu<br>-Deutsch<br>-English<br>-Español<br>-Français<br>-Italiano<br>-Latviesu<br>-Svenska |
| button link  | link to the repository github geneweb | |


### Advanced Options

| Feature              | Description                          | Options                           |
|----------------------|--------------------------------------|-----------------------------------|
| Clean up         | cleaning up a base after modifying it  | -all databases |
| Renaming         | change the name of a bases  | -all databases |
| Deletion         | delete a bases  | -all databases |
| Merging with other databases         | merge databases  | -all databases<br>-name resulting database |
| Saving and restoring         | redirect to page extract an import from GenWeb file  |  |
| initialisation of consanguinities         | initialization of consanguinities in a base  | -all databases<br>-Restart the computing from scratch. |
| Update links page / family chronicle         | start an operation "update_nldb" on the base selected  | -all databases |
| Compute connected componants         | Listing connected components  | -all database<br>-All connex components<br>-Produce connected components statistics<br>-Details for this length<br>-Ignore this file.<br>-By origin file.<br>-Ask for deleting branches whose size <= that value.<br>-Specifiy the number of branches to be deleted.<br>-Restrict deleting branches whose size = -del.<br>-Output results to this file/Output results in basename/notes_d/connex.txt (-o must stay empty and notes_d must exist)/No redirection of results. |
| Compute the difference between two bases         | Compute the difference between two bases  | -Select your first database: test,Starting person in first base.,Mandatory parameter,First name,Num,Surname<br>-Select your second database: test,Starting person in first base.,Mandatory parameter,First name,Num,Surname<br>-Checks descendants of all ascendants.<br>-Checks descendants (default).<br>-	Save memory space during operation (but it will be slower). |
| Fixes problems in a basedd         | Fix base and recompute index  | -all databases<br>-do not commit changes (only traces).<br>-quiet mode.<br>-very quiet mode.<br>	fast mode. Needs more memory<br>-families' parents.<br>-families' children.<br>-persons' NBDS.<br>-persons' parents.<br>-persons' families.<br>-pevents' witnesses.<br>-fevents' witnesses.<br>-marriage divorce.<br>-index. Automatically enabled by any other option,<br>-help |

### Configure

| Feature              | Description                          | Options                           |
|----------------------|--------------------------------------|-----------------------------------|
| The parameters of a database         | page where you can modify the parameters of a database  | -all database<br>-button configure<br>Second page:<br>-body prop modify style(color backgriund, text, link title...)<br>-default language<br>-Maximum level when displaying ancestors.<br>-Maximum level when displaying descendants.<br>-Maximum level when displaying ancestors by tree.<br>-Maximum level when displaying descendants by tree.<br>-History of updates<br>-Images path<br>-Hide advanced request.<br>-Password for "friends".<br>-Password for "Wizards".<br>-"Wizards" become simple "friend".<br>-Hide the private person's names.<br>-Ability to send images.<br>-Base has been renamed.<br>-add text at the bottom of each page<br>-Reorg mode |
| The parameters of the gwd service         | page where you can modify the parameters of the gwd service  | -Default language.<br>-Only authorized address.<br>-Connection log file. |
| Name and places cache files for auto completion.         | Produce cache files. | -all databases<br>-name of the folder holding databases<br>- First name<br>-Surnames<br>-Aliases<br>-Public names<br>-Qualifiers<br>-Places<br>-Add first name aliases to the first names list.<br>-Add surname aliases to the list of surnames<br>-Titles<br>-Domains<br>-Titles<br>-Occupations<br>-Sources<br>-Build all cache files.<br>-Show progress bar |

