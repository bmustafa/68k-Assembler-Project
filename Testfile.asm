* ASSEMBLY PROCESS EXAMPLE
* CONCORDIA SLIDES
           org         $000000
main      sub         d1,d1
           move       d1,a0
           move        24(a0),d0       ; this is a comment
           move        26(a0),d1       ; who cares?
           add         d1,d0
	   bra	       main
	   beq 	       main
           blt         main
           bgt         main
	   mulu       d1,d2
           divu       d1,d2
	   cmp        d1,d2
 	swap d1
          
           move        d0,28(a0)
           move        30(a0),d0

x          dc          11
           dc          -1
           ds          1
           dc          3
	   stop      #$2700
           end