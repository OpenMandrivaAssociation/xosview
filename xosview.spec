Summary: An X Window System utility for monitoring system resources
Name: xosview
Version: 1.8.0
Release: 8mdk
Exclusiveos: Linux
Url: http://xosview.sourceforge.net	
Source0: ftp://sunsite.unc.edu/pub/Linux/utils/status/xosview-%{version}.tar.bz2
Source2: %{name}16.png.bz2
Source3: %{name}32.png.bz2
Source4: %{name}48.png.bz2

Patch0: xosview-non-i386.patch.bz2
Patch1: xosview-io_h.patch.bz2
Patch2: xosview-ppc.patch.bz2
Patch3: xosview-rpath.patch.bz2
Patch5: xosview-1.7.1-s390.patch.bz2
Patch6: xosview-1.8.0-proc.patch.bz2
Patch7: xosview-kernel-pre9-patch.bz2
Patch8: xosview-PMUmeter-1.7.3.patch.bz2
Patch9: xosview-kernel-2.6.X.patch.bz2
Patch10: xosview-1.8.0-gcc33.patch.bz2

License: GPL
Group: Monitoring
Buildroot: %_tmppath/%{name}-root
BuildRequires: XFree86-devel
%ifarch alpha
BuildRequires: egcs
%endif
# XXX alpha barfs on linux/serial.h
ExcludeArch: alpha

%description
The xosview utility displays a set of bar graphs which show the current
system state, including memory usage, CPU usage, system load, etc.
Xosview runs under the X Window System.

Install the xosview package if you need a graphical tool for monitoring
your system's performance.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%ifarch ppc
# %patch2 -p0
%endif
%patch3 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p0
%patch9 -p1
%patch10 -p1 -b .gcc33
%ifarch ppc
%patch2 -p0
%patch8 -p1
%endif

# --- XXX Cruft Alert!
rm -f linux/*.o

%build
#remove rpath in LFLAGS
cd config; make; cd ..
# can't build both 2.0.x/2.1.x memstat modules
%ifnarch alpha
CXXFLAGS="$RPM_OPT_FLAGS -Wno-deprecated" %configure --disable-linux-memstat --enable-linux-syscalls ; make
%else
CXX="g++ -V`egcs-version`" 
CXXFLAGS="$RPM_OPT_FLAGS -Wno-deprecated" %configure --disable-linux-memstat --enable-linux-syscalls ; make CXX="g++ -V`egcs-version`"  
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/X11R6/{bin,man/man1,lib/X11/app-defaults}

make PREFIX_TO_USE=$RPM_BUILD_ROOT/usr/X11R6 install

chmod u-s $RPM_BUILD_ROOT/usr/X11R6/bin/*

install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/icons/mini
bzcat %SOURCE2 > $RPM_BUILD_ROOT%{_datadir}/icons/mini/%{name}.png
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/icons
bzcat %SOURCE3 > $RPM_BUILD_ROOT%{_datadir}/icons/%{name}.png
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/icons/large
bzcat %SOURCE4 > $RPM_BUILD_ROOT%{_datadir}/icons/large/%{name}.png

(cd $RPM_BUILD_ROOT
mkdir -p ./%{_menudir}
cat > ./%{_menudir}/%{name} <<EOF
?package(%{name}):\
needs="X11"\
section="Applications/Monitoring"\
title="Xosview"\
longtitle="OS stats viewer"\
command="%{name}"\
icon="%{name}.png"
EOF
)


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%{_prefix}/X11R6/bin/*
%{_prefix}/X11R6/man/man1/*
%{_prefix}/X11R6/lib/X11/app-defaults/*
%{_menudir}/*
%{_datadir}/icons/%{name}.png
%{_datadir}/icons/mini/*
%{_datadir}/icons/large/*

%post
%update_menus

%postun
%clean_menus
