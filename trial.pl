$|=1;
# Pipe version: Input in STDIN, to STDOUT. Will eat input file provided as first param as well.
# if ( -f $ARGV[0] ) { open(IN,"$ARGV[0]") or die }
# else { open(IN,STDIN) or die }
# open(IN,"trial.csv") or die;
open($in,"$ARGV[0]") or $in=\*STDIN or die "Cannot read input..";
# while(<IN>){
while(<$in>){
	chomp; next if /^No/;	# Skip title - all are fixed type records anyway.
	s/\s+,/,/g; s/,\s+/,/g; s/\s+$//;	# Sanitisation.
	my (undef,$room,$sn,$name,$rn,$slot,$subj)=split(/,/);
	#my (undef,$room,$sn,$slot,$subj,$rn,$name)=split(/,/);
	$room{$room}{$subj}++; $subj{$subj}++; $room_total{$room}++; $total++;
};
$sep='","';	# For joining lists to neater CSVs.
@subj=sort keys %subj;
$title='"'.join($sep,"Room",@subj,"Total").'"'; 

# open($out,">","trial-out.csv") or die;	# Here is where our output goes.
$out=\*STDOUT;
print $out "$title\n";

foreach $room ( sort keys %room ) {
	@det=(); $det=undef;
	push(@det,$room);
	foreach $subj ( @subj ) {
		push(@det,$room{$room}{$subj}?$room{$room}{$subj}:0);
	}
	$det='"'.join($sep,@det,$room_total{$room}).'"';
	print $out "$det\n";
}
push(@sum,'Total');
foreach $subj ( sort keys %subj ) {
	push(@sum,$subj{$subj});
} $sum='"'.join($sep,@sum,$total).'"';
print $out $sum,"\n";
close IN, $out;
