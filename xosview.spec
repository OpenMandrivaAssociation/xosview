Summary: An X Window System utility for monitoring system resources
Name: xosview
Version: 1.8.3
Release: %mkrel 2
Exclusiveos: Linux
Url: http://xosview.sourceforge.net	
Source0: http://dl.sourceforge.net/sourceforge/xosview/xosview-%{version}.tar.gz
Source2: %{name}16.png.bz2
Source3: %{name}32.png.bz2
Source4: %{name}48.png.bz2

License: GPL
Group: Monitoring
Buildroot: %_tmppath/%{name}-root
BuildRequires: libxdmcp-devel
BuildRequires: libxau-devel
BuildRequires: libx11-devel
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

# --- XXX Cruft Alert!
rm -f linux/*.o

%build
cd config; make; cd ..
# can't build both 2.0.x/2.1.x memstat modules
%ifnarch alpha
CXXFLAGS="$RPM_OPT_FLAGS -Wno-deprecated -DHAVE_SNPRINTF" %configure --disable-linux-memstat --enable-linux-syscalls ; make
%else
CXX="g++ -V`egcs-version`" 
CXXFLAGS="$RPM_OPT_FLAGS -Wno-deprecated" %configure --disable-linux-memstat --enable-linux-syscalls ; make CXX="g++ -V`egcs-version`"  
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,share/man/man1,lib/X11/app-defaults}

make PREFIX_TO_USE=$RPM_BUILD_ROOT/usr install

chmod u-s $RPM_BUILD_ROOT/usr/bin/*

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
section="System/Monitoring"\
title="Xosview"\
longtitle="OS stats viewer"\
command="%{name}"\
icon="%{name}.png"\
xdg="true"
EOF
)
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Xosview
Comment=System resources monitor for X11
Exec=%{_bindir}/xosview
Icon=%{name}
Terminal=false
Type=Application
Categories=System;Monitor;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%{_prefix}/bin/*
%{_prefix}/share/man/man1/*
%{_prefix}/lib/X11/app-defaults/*
%{_menudir}/*
%{_datadir}/icons/%{name}.png
%{_datadir}/icons/mini/*
%{_datadir}/icons/large/*
%{_datadir}/applications/mandriva-%{name}.desktop

%post
%update_menus

%postun
%clean_menus
