%define modname yaml
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B13_%{modname}.ini

Summary:	YAML-1.1 parser and emitter
Name:		php-%{modname}
Version:	1.1.0
Release:	%mkrel 1
Group:		Development/PHP
License:	MIT
URL:		http://pecl.php.net/package/yaml/
Source0:	http://pecl.php.net/get/yaml-%{version}.tgz
Source1:	B13_yaml.ini
BuildRequires:	pkgconfig
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	yaml-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Support for YAML 1.1 (YAML Ain't Markup Language) serialization using the
LibYAML library.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml tests
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-1mdv2012.0
+ Revision: 806420
- 1.1.0

* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-6
+ Revision: 795532
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-5
+ Revision: 761347
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-4
+ Revision: 696491
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-3
+ Revision: 695492
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2
+ Revision: 646706
- rebuilt for php-5.3.6

* Mon Feb 21 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1
+ Revision: 639162
- import php-yaml


* Mon Feb 21 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2010.2
- initial Mandriva package
