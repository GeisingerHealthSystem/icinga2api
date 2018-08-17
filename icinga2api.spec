%define name icinga2api
%define version 0.6.0
%define unmangled_version 0.6.0
%define unmangled_version 0.6.0
%define release 1

Summary: Python Icinga 2 API
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: 2-Clause BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: fmnisme, Tobias von der Krone <fmnisme@gmail.com, tobias@vonderkrone.info>
Url: https://github.com/tobiasvdk/icinga2api

%description
# <a id="about-icinga2"></a> About icinga2api

icinga2api is a [Python](http://www.python.org) module to interact with the [Icinga 2 RESTful API](https://www.icinga.com/docs/icinga2/latest/doc/12-icinga2-api/).

# Features

1. [basic and certificate auth](doc/2-authentication.md)
1. [config file support](doc/2-authentication.md#-config-file)
1. [objects (zone support)](doc/3-objects.md)
1. [actions](doc/4-actions.md)
1. [events](doc/5-events.md)
1. [status](doc/6-status.md)

# Developing

1. Code cleanup
1. Tests
1. Configuration Management

# Usage

See the [doc](doc) directory.


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
