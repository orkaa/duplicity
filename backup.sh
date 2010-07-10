#!/bin/bash

HELP="Use backup for normal backup\n
full to force full backup\n
rotate-view to view old sets\n 
rotate-force to actually delete old sets\n
status to view current backup sets status "
######################################## CONFIG ################################################
### The gpg key you want to use and a passphrase for it.
#SIGNKEY=208V76D4
#ENCKEY=$SIGNKEY
#export PASSPHRASE=''

# How old should the backups be before deleted. 
FULLBACKUPS="2"

# Where to backup? Can be local or remote path.
TARGET="file:///mnt/backup"
#TARGET="scp://user@hostname//mnt/backup"

# Directories you want to include.
DIRS="--include /etc  
	--include /var"

# Directories you want to exclude.
EDIRS="--exclude /porn
	--exclude /proc"

# Additional ssh options.
#SSH_OPTIONS="--ssh-options=\"-oPort=1234\""

# Encryption yes/no ?
ENCRYPTION="--no-encryption"
#ENCRYPTION="--encrypt-key $ENCKEY --sign-key $SIGNKEY"

# If you don't have enough space for temp files on /, use this.
export TMPDIR=/var/duplicity_tmp

#################### CONFIG END #############################################

#### LOCK FILE IMPLEMENTATION ####
if [ -f /var/tmp/duplicity ]; then
	echo "Duplicity already running!"
	exit
else
	touch /var/tmp/duplicity
fi

case $1 in
"backup")
duplicity \
   $ENCRYPTION \
   $SSH_OPTIONS \
   --volsize 100  \
   $EDIRS \
   $DIRS \
   --exclude '**' / \
   $TARGET
;;

"full")    
duplicity full \
   $ENCRYPTION \
   $SSH_OPTIONS \
   --volsize 100  \
   $EDIRS \
   $DIRS \
   --exclude '**' / \
   $TARGET
;;

"rotate-view") 
duplicity remove-all-but-n-full $FULLBACKUPS \
   $ENCRYPTION \
   $SSH_OPTIONS \
   $TARGET
;;

"rotate-force") 
duplicity remove-all-but-n-full $FULLBACKUPS \
   $ENCRYPTION \
   $SSH_OPTIONS \
    --force \
   $TARGET
;;

"status")
duplicity collection-status \
   $ENCRYPTION \
   $SSH_OPTIONS \
    $TARGET
;;

"cleanup")
duplicity cleanup \
   $ENCRYPTION \
   $SSH_OPTIONS \
   --force \
   $TARGET
;;

"help")
echo -e $HELP
;;

*)
echo "Use help for usage tips"
;;
esac
### clean up
rm -f /var/tmp/duplicity
