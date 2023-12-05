#!/bin/bash
# accepts input from stdin
# set $first_part to 0 for second part
perl -ne '
BEGIN {
    $first_part = 1;
    %digit_map = (
        one => "1", two => "2", "three" => "3", "four" => "4", "five" => "5", "six" => "6", "seven" => "7", "eight" => "8", "nine" => "9"
    );
    $regex = "(" . join("|", keys(%digit_map)) . ")";
}
if ($first_part) {
    $regex = 'wont-match-anything';
}

chomp($orig = $_);
if (/^\D*?$regex/g) {
    my $match = $1;
    my $replacement = $digit_map{$1};
    # print "replacing first $match -> $replacement in $_";
    s,$match,$replacement,;
}
if (/.*$regex/g) {
    my $match = $1;
    my $replacement = $digit_map{$1};
    # print "replacing last $match -> $replacement in $_";
    s,(.*)$match,\1$replacement,;
}
# print "$orig -> text: $_";
($f = $_) =~ s,^\D*(\d).*,\1,;
($l = $_) =~ s,.*(\d)\D*$,\1,;
# print "$orig -> int: ", (int($f)*10+int($l)), "\n";
$s += int($f)*10+int($l);
END{
    print $s;
}'
