%define srcname flit

Name:		python-%{srcname}
Version:	2.1.0
Release:	1
Summary:	Simplified packaging of Python modules

# ./flit/logo.py  under ASL 2.0 license
# ./flit/upload.py under PSF license
License:	BSD and ASL 2.0 and Python
Group:          Development/Python
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

%description
Flit is a simple way to put Python packages and modules on PyPI.

Flit only creates packages in the new 'wheel' format. People using older
versions of pip (<1.5) or easy_install will not be able to install them.

Flit packages a single importable module or package at a time, using the import
name as the name on PyPI. All sub-packages and data files within a package are
included automatically.

Flit requires Python 3, but you can use it to distribute modules for Python 2,
so long as they can be imported on Python 3.

%package -n python-%{srcname}-core
Group:		Development/Python
Summary:	PEP 517 build backend for packages using Flit
%{?python_provide:%python_provide python-%{srcname}-core}
Conflicts:	python-%{srcname} < 2.1.0-2

%description -n python-%{srcname}-core
This provides a PEP 517 build backend for packages using Flit.
The only public interface is the API specified by PEP 517,
at flit_core.buildapi.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
export FLIT_NO_NETWORK=1
# first, build flit_core with self
# TODO do it in a less hacky way, this is reconstructed from pyoroject.toml
cd flit_core
PYTHONPATH=$(pwd) %{__python} -c 'from flit_core.build_thyself import build_wheel; build_wheel(".")'

# %%py3_install_wheel unfortunately hardcodes installing from dist/
mkdir ../dist
mv flit_core-%{version}-py2.py3-none-any.whl ../dist
cd -

PYTHONPATH=$(pwd):$(pwd)/flit_core %{__python3} -m flit build --format wheel

%install
%py3_install

%files
%license LICENSE
%doc README.rst
#{python_sitelib}/flit-*.dist-info/
#{python_sitelib}/flit/
#{_bindir}/flit


%files -n python-%{srcname}-core
%license LICENSE
%doc flit_core/README.rst
#{python_sitelib}/flit_core-*.dist-info/
#{python_sitelib}/flit_core/
