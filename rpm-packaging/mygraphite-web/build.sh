#!/bin/sh

if [ -z "$GRAPHITE_VERSION" ]; then
  GRAPHITE_VERSION=0.9.11
fi

if [ -z "$GRAPHITE_HIGH_VERSION" ]; then
  GRAPHITE_HIGH_VERSION=0.9
fi

if [ $# -gt 1 ]; then
 GRAPHITE_VERSION=$1
 shift
fi

if [ $# -gt 1 ]; then
 GRAPHITE_HIGH_VERSION=$1
 shift
fi


GRAPHITE_URL=http://launchpad.net/graphite/$GRAPHITE_HIGH_VERSION/$GRAPHITE_VERSION/+download/graphite-web-$GRAPHITE_VERSION.tar.gz

download_file_if_needed()
{
	URL=$1
	DEST=$2

	if [ ! -f $DEST ]; then

		echo "downloading from $URL to $DEST..."
		curl -L $URL -o $DEST

		case $DEST in
			*.tar.gz)
	        	tar tzf $DEST >>/dev/null 2>&1
	        	;;
	    	*.zip)
	        	unzip -t $DEST >>/dev/null 2>&1
	        	;;
	    	*.jar)
	        	unzip -t $DEST >>/dev/null 2>&1
	        	;;
	    	*.war)
	        	unzip -t $DEST >>/dev/null 2>&1
	        	;;
		esac

		if [ $? != 0 ]; then
			rm -f $DEST
			echo "invalid content for `basename $DEST` downloaded from $URL, discarding content and aborting build."
			exit -1
		fi

	fi
}

download_file_if_needed $GRAPHITE_URL SOURCES/graphite-web-${GRAPHITE_VERSION}.tar.gz

echo "Version to package is $GRAPHITE_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="GRAPHITE_REL $GRAPHITE_VERSION"  SPECS/mygraphite-web.spec
