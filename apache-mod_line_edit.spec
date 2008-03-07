#Module-Specific definitions
%define mod_name mod_line_edit
%define mod_conf A95_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A general-purpose output filter for text documents for Apache
Name:		apache-%{mod_name}
Version:	1.0.0
Release:	%mkrel 3
Group:		System/Servers
License:	GPL
URL:		http://apache.webthing.com/mod_line_edit/
Source0:	http://apache.webthing.com/mod_line_edit/mod_line_edit.c
Source1:	%{mod_conf}
Source2:	http://apache.webthing.com/mod_line_edit/index.html
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_line_edit is a general-purpose filter for text documents. It operates as a
simple on-the-fly line editor, applying search-and-replace rules defined in a
configuration or .htaccess file.

Unlike most of Webing's filter modules, it is not markup-aware, so it is not an
optimal choice for processing HTML or XML, though it may nevertheless be used
with caution (and may be far better than semi-markup-aware options such as
mod_layout).

For non-markup document types such as plain text, and non-markup Web documents
such as Javascript or Stylesheets, it is the best available option in the
absence of a filter that parses any relevant document structures.

mod_line_edit is written for performance and reliability, and should scale
without problems as document size grows. mod_line_edit is fully compatible with
Apache 2.0 and 2.2, and all operating systems and MPMs.

%prep

%setup -q -T -c -n %{mod_name}-%{version}
cp %{SOURCE0} %{mod_name}.c
cp %{SOURCE1} %{mod_conf}
cp %{SOURCE2} README.html

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

head -19 %{mod_name}.c > LICENSE

%build
%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


