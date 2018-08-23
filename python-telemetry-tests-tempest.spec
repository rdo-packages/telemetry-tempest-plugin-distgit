%{!?upstream_version: %global upstream_version %{commit}}
%global commit b35146e1a423e81b2bbdd8621d0310ffac9af517
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%global service telemetry
%global plugin telemetry-tempest-plugin
%global module telemetry_tempest_plugin
%global with_doc 1

%if 0%{?fedora}
%global with_python3 1
%endif


%if 0%{?dlrn}
%define tarsources %module
%else
%define tarsources %plugin
%endif

%global common_desc \
This package contains Tempest tests to cover the telemetry projects. \
Additionally it provides a plugin to automatically load these tests\
into Tempest.

Name:       python-%{service}-tests-tempest
Version:    0.0.1
Release:    0.2%{?alphatag}%{?dist}
Summary:    Tempest Integration of Telemetry Project
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://github.com/openstack/%{plugin}/archive/%{commit}.tar.gz#/%{plugin}-%{shortcommit}.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}-tests-tempest}
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools

Obsoletes:   python-panko-tests < 4.0.0
Obsoletes:   python-gnocchi-tests < 4.2.0
Obsoletes:   python-aodh-tests < 6.0.0
Obsoletes:   python-ceilometer-tests < 1:10.0.0

Requires:   python2-pbr >= 3.1.1
Requires:   python2-six >= 1.10.0
Requires:   python2-tempest >= 1:18.0.0
Requires:   python2-oslo-config >= 2:5.2.0
Requires:   python2-oslo-utils >= 3.33.0
Requires:   python2-gabbi >= 1.42.1
Requires:   python2-ujson >= 1.35
Requires:   python2-heat-tests-tempest

%description -n python2-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        Telemetry Tempest Plugin documentation

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the telemetry tempest plugin.
%endif

%if 0%{?with_python3}
%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-pbr >= 3.1.1
Requires:   python3-six >= 1.10.0
Requires:   python3-tempest >= 1:18.0.0
Requires:   python3-oslo-config >= 2:5.2.0
Requires:   python3-oslo-utils >= 3.33.0
Requires:   python3-gabbi >= 1.42.1
Requires:   python3-ujson >= 1.35
Requires:   python3-heat-tests-tempest

%description -n python3-%{service}-tests-tempest
%{common_desc}
%endif

%prep
%autosetup -n %{tarsources}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%files -n python2-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Thu Aug 23 2018 Chandan Kumar <chkumar@redhat.com> 0.0.1-0.2.b35146e1git
- Update to pre-release 0.0.1 (b35146e1a423e81b2bbdd8621d0310ffac9af517)
