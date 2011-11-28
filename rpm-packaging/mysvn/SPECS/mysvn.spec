Name: mysvn
Version: 1.0.0
Release: 1
Summary: Subversion setup
Group: Company/Development
URL: http://www.mycorp.org/
Vendor: MyCorp
Packager: MyCorp
License: AGPLv1
BuildArch:  noarch

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

# we want apache2 in worker mode (subversion Requires apache2 only)
Requires: apache2-worker
Requires: subversion-server
Requires: viewvc

Source0: httpd-svn.conf
Source1: private_access_rules
Source2: private_access_passwords

%description
Subversion setup for MyCorp

%prep

%build

%install
# Prep the install location.
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/mysvn/repos

cp %{SOURCE0}  $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d/svn.mycorp.org.conf
cp %{SOURCE1}  $RPM_BUILD_ROOT%{_var}/lib/mysvn/repos
cp %{SOURCE2}  $RPM_BUILD_ROOT%{_var}/lib/mysvn/repos

%post
if [ "$1" == "1" ]; then
  pushd %{_var}/lib/mysvn/repos >>/dev/null
  echo "creating public repo"
  svnadmin create public
  chown -R wwwrun:www %{_var}/lib/mysvn/repos/public
  echo "creating private repo"
  svnadmin create private
  chown -R wwwrun:www %{_var}/lib/mysvn/repos/private
  popd >>/dev/null

  # Enable Apache modules for SVN
  a2enmod dav
  a2enmod dav_fs
  a2enmod dav_svn
  a2enmod authnz_ldap
  a2enmod authz_svn
  a2enmod ldap

  # Enable ViewVC
  a2enflag SVN_VIEWCVS

  service apache2 restart
fi


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/apache2/vhosts.d/svn.mycorp.org.conf
%{_var}/lib/mysvn/repos
%{_var}/lib/mysvn/repos/private_access_rules
%{_var}/lib/mysvn/repos/private_access_passwords


%changelog
* Wed Mar 23 2009 henri.gomez@gmail.com 1.0.0-1
- Initial RPM