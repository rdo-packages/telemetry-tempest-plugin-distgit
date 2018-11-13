# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global service telemetry
%global plugin telemetry-tempest-plugin
%global module telemetry_tempest_plugin
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
This package contains Tempest tests to cover the telemetry projects. \
Additionally it provides a plugin to automatically load these tests\
into Tempest.

Name:       python-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of Telemetry Project
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python%{pyver}-%{service}-tests-tempest}
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools

Obsoletes:   python-panko-tests < 4.0.0
Obsoletes:   python-gnocchi-tests < 4.2.0
Obsoletes:   python-aodh-tests < 6.0.0
Obsoletes:   python-ceilometer-tests < 1:10.0.0

Requires:   python%{pyver}-pbr >= 3.1.1
Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-tempest >= 1:18.0.0
Requires:   python%{pyver}-oslo-config >= 2:5.2.0
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-gabbi >= 1.42.1
Requires:   python%{pyver}-ujson >= 1.35
Requires:   python%{pyver}-heat-tests-tempest

%description -n python%{pyver}-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        Telemetry Tempest Plugin documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the telemetry tempest plugin.
%endif

%prep
%autosetup -n %{module}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%{pyver_build}

# Generate Docs
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%files -n python%{pyver}-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
