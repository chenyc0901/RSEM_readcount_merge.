#! /bin/bash


arr=($(ls ../Clean_read/*.fq.gz|cut -d "/" -f 3|awk '{split($1,a,"_");print a[1]"_"a[2]}'|sort|uniq))
for file in ${arr[@]};
do
    echo "${file} processing"
   rsem-calculate-expression --paired-end \
                               --star \
                               --star-gzipped-read-file \
                               -p 20 \
                               ../Clean_read/${file}_trimmed_1.fq.gz \
                               ../Clean_read/${file}_trimmed_2.fq.gz \
                               ../../../ref/STAR_index \
                               ${file}_RSEM
done
