%{?scl:%scl_package jctools}
%{!?scl:%global pkg_name %{name}}

%global namedreltag %nil
%global namedversion %{version}%{?namedreltag}

Name:		%{?scl_prefix}jctools
Version:	1.2.1
Release:	3%{?dist}
Summary:	Java Concurrency Tools for the JVM
License:	ASL 2.0
URL:		http://jctools.github.io/JCTools/
Source0:	https://github.com/JCTools/JCTools/archive/v%{namedversion}/%{pkg_name}-%{namedversion}.tar.gz

# nasty hack TODO
BuildRequires:	java-devel-openjdk >= 1:1.8.0
Requires:	java-devel-openjdk >= 1:1.8.0
BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:	%{?scl_prefix_java_common}junit
BuildRequires:	%{?scl_prefix_java_common}hamcrest
BuildRequires:  %{?scl_prefix_java_common}objectweb-asm%{?scl:5}
%{?scl:Requires: %scl_runtime}
BuildArch:	noarch

%description
This project aims to offer some concurrent data structures
currently missing from the JDK:

° SPSC/MPSC/SPMC/MPMC Bounded lock free queues
° SPSC/MPSC Unbounded lock free queues
° Alternative interfaces for queues
° Offheap concurrent ring buffer for ITC/IPC purposes
° Single Writer Map/Set implementations
° Low contention stats counters
° Executor

%package experimental
Summary:	JCTools Experimental implementations

%description experimental
Experimental implementations for the
Java Concurrency Tools Library.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%package parent
Summary:	JCTools Parent POM

%description parent
JCTools Parent POM.

%prep
%setup -q -n JCTools-%{namedversion}
# Cleanup
find . -name '*.class' -print -delete
find . -name '*.jar' -print -delete

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_xpath_set pom:project/pom:version %{namedversion}
%pom_xpath_set -r pom:parent/pom:version %{namedversion} %{pkg_name}-core %{pkg_name}-experimental

# Prevent build failure
%pom_remove_plugin :maven-enforcer-plugin

# Unavailable deps
%pom_disable_module %{pkg_name}-benchmarks

# Not available
%pom_remove_plugin :cobertura-maven-plugin %{pkg_name}-core

# Useless tasks
%pom_remove_plugin :maven-source-plugin %{pkg_name}-core
%pom_xpath_remove "pom:plugin[pom:artifactId = 'maven-javadoc-plugin']/pom:executions" %{pkg_name}-core

# lower the version requirement for objectweb-asm in scl package
%{?scl:%pom_change_dep :asm-all:5.0.4 :asm-all:5.0.3 %{pkg_name}-experimental}

# Add OSGi support
for mod in core experimental; do
 %pom_xpath_set "pom:project/pom:packaging" bundle %{pkg_name}-${mod}
 %pom_add_plugin org.apache.felix:maven-bundle-plugin:2.3.7 %{pkg_name}-${mod} '
 <extensions>true</extensions>
 <executions>
   <execution>
     <id>bundle-manifest</id>
     <phase>process-classes</phase>
     <goals>
       <goal>manifest</goal>
     </goals>
   </execution>
 </executions>
 <configuration>
  <excludeDependencies>true</excludeDependencies>
 </configuration>'
done
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -s
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles-%{pkg_name}-core
%doc README.md
%license LICENSE

%files experimental -f .mfiles-%{pkg_name}-experimental

%files javadoc -f .mfiles-javadoc
%license LICENSE

%files parent -f .mfiles-%{pkg_name}-parent
%license LICENSE

%changelog
* Wed Feb 15 2017 Tomas Repik <trepik@redhat.com> - 1.2.1-3
- scl conversion

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 28 2016 gil cattaneo <puntogil@libero.it> 1.2.1-1
- update to 1.2.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 gil cattaneo <puntogil@libero.it> 1.1-0.1.alpha
- initial rpm
