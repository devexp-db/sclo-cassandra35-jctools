%global namedreltag -alpha
%global namedversion %{version}%{?namedreltag}

Name:          jctools
Version:       1.1
Release:       0.1.alpha%{?dist}
Summary:       Java Concurrency Tools for the JVM
License:       ASL 2.0
URL:           http://jctools.github.io/JCTools/
Source0:       https://github.com/JCTools/JCTools/archive/v%{namedversion}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.hamcrest:hamcrest-all)
BuildRequires: mvn(org.ow2.asm:asm-all)

BuildArch:     noarch

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

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n JCTools-%{namedversion}
# Cleanup
find . -name '*.class' -print -delete
find . -name '*.jar' -print -delete

# Prevent build failure
%pom_remove_plugin :maven-enforcer-plugin

# Unavailable deps
%pom_disable_module jctools-benchmarks

# Add OSGi support
%pom_xpath_set "pom:project/pom:packaging" bundle jctools-core
%pom_add_plugin org.apache.felix:maven-bundle-plugin:2.3.7 jctools-core '
<extensions>true</extensions>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>'

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Tue May 19 2015 gil cattaneo <puntogil@libero.it> 1.1-0.1.alpha
- initial rpm
