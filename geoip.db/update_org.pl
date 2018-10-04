#!/usr/bin/perl
use DBI;
use Geo::IP;
use Geo::IPfree;

%config =( database=> 'mydns', table=> 'geoip', domain_table => 'soa', db_host=> 'localhost', db_user=>'root', db_pass => '');

my $gi = Geo::IP->open("/home/resolver/geoIP_org/db/GeoIPOrg.dat", GEOIP_STANDARD);
my $gic = Geo::IPfree->new;

my $database = "DBI:mysql:database=$config{database};host=$config{db_host};";
$dbh = DBI->connect ($database,$config{db_user},$config{db_pass});
my $query = $dbh->prepare("select id,zone,data from rr where type='A'");
$query->execute();

while (($id,$zone,$ip) = $query->fetchrow_array()) {
	my $org = $gi->org_by_name($ip);
	my ($country,$cname) = $gic->LookUp($ip);
	print "org: $org country: $country\n";
	my $ins = $dbh->prepare("insert into rr_geo (id,zone,org,country) values(?,?,?,?)");
	$ins->execute("$id","$zone","$org","$country");
}

