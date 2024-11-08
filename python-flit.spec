%define srcname flit

Name:		python-%{srcname}
Version:	3.10.1
Release:	1
Summary:	Simplified packaging of Python modules

# ./flit/logo.py under ASL 2.0 license
# ./flit/upload.py under PSF license
License:	BSD and ASL 2.0 and Python
Group:		Development/Python
URL:		https://flit.readthedocs.io/en/latest/
Source0:	https://pypi.io/packages/source/f/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(pip)
BuildRequires:	python3dist(requests)
BuildRequires:	python3dist(docutils)
BuildRequires:	python3dist(pygments)
BuildRequires:	python3dist(idna)
BuildRequires:	python3dist(certifi)
BuildRequires:	python3dist(urllib3)
BuildRequires:	python3dist(chardet)
BuildRequires:	python3dist(pytoml)
BuildRequires:	python3dist(wheel)

%description
Flit is a simple way to put Python packages and modules on PyPI.

Flit only creates packages in the new 'wheel' format. People using older
versions of pip (<1.5) or easy_install will not be able to install them.

Flit packages a single importable module or package at a time, using the import
name as the name on PyPI. All sub-packages and data files within a package are
included automatically.

Flit requires Python 3, but you can use it to distribute modules for Python 2,
so long as they can be imported on Python 3.

%files
%license LICENSE
%doc README.rst
%{python_sitelib}/flit-*.dist-info/
%{python_sitelib}/flit/
%{_bindir}/flit

#----------------------------------------------------------------------------

%package -n python-%{srcname}-core
Group:		Development/Python
Summary:	PEP 517 build backend for packages using Flit
%{?python_provide:%python_provide python-%{srcname}-core}
Conflicts:	python-%{srcname} < 2.1.0-2
Provides:	python-tomli

%description -n python-%{srcname}-core
This provides a PEP 517 build backend for packages using Flit.
The only public interface is the API specified by PEP 517,
at flit_core.buildapi.

%files -n python-%{srcname}-core
%license LICENSE
%doc flit_core/README.rst
%{python_sitelib}/flit_core-*.dist-info/
%{python_sitelib}/flit_core/

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
export FLIT_NO_NETWORK=1
cd flit_core

%{__python3} -m pip wheel --wheel-dir %{_builddir} --no-deps --use-pep517 --no-build-isolation \
			 --disable-pip-version-check --no-clean --progress-bar off --verbose .
cd -

export PYTHONPATH=$PWD:$PWD/flit_core

%{__python3} -m pip wheel --wheel-dir %{_builddir} --no-deps --use-pep517 --no-build-isolation \
			 --disable-pip-version-check --no-clean --progress-bar off --verbose .


%install
cd -

%{__python3} -m pip install --root %{buildroot} --no-deps --disable-pip-version-check --progress-bar off \
			--verbose --ignore-installed --no-warn-script-location --no-index --no-cache-dir \
			--find-links %{_builddir} *.whl

