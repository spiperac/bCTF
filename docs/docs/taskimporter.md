# Task importer

Task improter is a feature of bCTF that can be found in Admin panel, and it can be used to automaticly import challenges you prepared for competition from .ZIP file.
It will create categories, create challenges, add flags, files and points for you.
It's really useful for automation of your competition, and it also helps you to better organise your challenges repository.

## Challenges .ZIP structure

As mentioned, challenges have to be imported from non-password protected .ZIP file.
Folder structure of your challenges repository should be fairly simple in order for Task Importer to recogise and import it.

Here's example:

<pre>
| Root
|
|--------| Challenge 1
|		 |
|		 |- task.yml
|		 |
|		 |- files/
|
|
|
|--------| Challenge 2
|		 |
|		 |- task.yml
|		 |
|		 |- files/ |
|				   | - example.c
|
|
|--------| Challenge 3
|		 |
|		 |- task.yml
|		 |
|		 |- files/


</pre>


So, your folder with challenges should contain one challenge directory per challenge. TaskImporter will consider every folder as a new challenge.
Inside challenge directory, you will need to have <b>task.yml</b> file which holds description and definition of your task.

<b>task.yml</b>
<pre>
name: Challenge 2
author: hax0r
category: example
description: Some misleading description
points: 150
flag: bctf{flag_imposible_to_guess}
attachments:
  - example.c

</pre>

As you may guess, in section attachments you have to define which files you want to be uploaded as attachment for that specific task. In example above, there's <b>example.c</b>.
That means that Task Importer will try to upload file from <b>challenge2/files/example.c</b>.


Note: On error, or improperly configured task, Task Importer will skip that challenge and contrinue to import others.