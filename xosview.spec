Summary: An X Window System utility for monitoring system resources
Name: xosview
Version: 1.16
Release: 2
Exclusiveos: Linux
Url: http://xosview.sourceforge.net	
Source0: http://www.pogo.org.uk/~mark/xosview/releases/%{name}-%{version}.tar.gz
Source2: %{name}16.png.bz2
Source3: %{name}32.png.bz2
Source4: %{name}48.png.bz2

License: GPLv2+
Group: Monitoring
BuildRequires: pkgconfig(xdmcp)
BuildRequires: pkgconfig(xau)
BuildRequires: pkgconfig(xpm)
BuildRequires: pkgconfig(x11)
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

sed -e 's:lib/X11/app:share/X11/app:g' \
	-i xosview.1 || die

%build
%setup_compile_flags
%make

%install
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_mandir}/man1/
make PREFIX=%{buildroot}/usr install

chmod u-s %{buildroot}/usr/bin/*



mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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

%files
%defattr(-,root,root,0755)
%{_prefix}/bin/*
%{_prefix}/share/man/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
