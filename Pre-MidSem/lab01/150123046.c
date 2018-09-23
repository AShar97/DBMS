#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STRING 100

struct data_entry{
	unsigned int rollno;
	char note[MAX_STRING];
};

struct data_out{
	unsigned int rollno;
	unsigned int present;
	unsigned int absent;
};

int comparator(const void *p, const void *q) 
{
    unsigned int l = ((struct data_entry *)p)->rollno;
    unsigned int r = ((struct data_entry *)q)->rollno; 
    return (l - r);
}

unsigned int file_lines(char* filename){
	FILE *fp;
    unsigned int count = 0;  // Line counter (result)
    char c;  // To store a character read from file
 
    // Open the file
    fp = fopen(filename, "r");
 
    // Check if file exists
    if (fp == NULL)
    {
        printf("Could not open file %s", filename);
        return 0;
    }
 
    // Extract characters from file and store in character c
    for (c = getc(fp); c != EOF; c = getc(fp))
        if (c == '\n') // Increment count if this character is newline
            count = count + 1;
 
    // Close the file
    fclose(fp);
    return(count);
 }

struct data_entry* data_read(char* filename, unsigned int count, struct data_entry* data_in){
	FILE *fp;
    fp = fopen(filename, "r");
 
    // Check if file exists
    if (fp == NULL)
    {
        printf("Could not open file %s", filename);
        return 0;
    }
 	
 	// Extract data from file and store in data_in
    for (unsigned int i=0; i<count; i++){
    	fscanf(fp, "%u%*c%*s%s", &(data_in[i].rollno), (data_in[i].note));
    }
 
    // Close the file
    fclose(fp);

    qsort((void*)data_in, count, sizeof(data_in[0]), comparator);

    return(data_in);
}

struct data_out* manipulate(struct data_entry* data_in, unsigned int* count, struct data_out* data){
	unsigned int j = 0;

	for (unsigned int i=0; i < *count; i++){
		if (i!=0 && data_in[i].rollno != data_in[i-1].rollno){
			j++;
			data[j].rollno = data_in[i].rollno;
		}
		if (i==0){
			data[j].rollno = data_in[i].rollno;
		}

		if (strcmp(data_in[i].note,"Present")==0){
			data[j].present++;
		}
		else {
			if (strcmp(data_in[i].note,"Absent")==0){
				data[j].absent++;
			}
		}
	}

	*count = j+1;

	return(data);
}

void generate(struct data_out* data, unsigned int count,  char* out_l, char* out_g){
	FILE * fg; FILE * fl;
	fg = fopen(out_g, "w+");
 
    fl = fopen(out_l, "w+");

    float percent = 0;

    for (unsigned int i=0; i<count; i++){
    	percent = (float)data[i].present/(data[i].present+data[i].absent);
    	if(percent >= 0.75){
    		fprintf(fg, "%u, %u, %f\n", data[i].rollno, data[i].present, percent*100.0);
    	}
    	else{
    		fprintf(fl, "%u, %u, %f\n", data[i].rollno, data[i].present, percent*100.0);
    	}
    }

    fclose(fl); fclose(fg);
}

void database(char* filename, char* out_l, char* out_g){
	unsigned int count = file_lines(filename);
	
	struct data_entry data_in[count];
	for (unsigned int i=0; i < count; i++){
		data_in[i].rollno = 0;
		(data_in[i].note)[0] = '\0';
	}
	data_read(filename, count, data_in);

	struct data_out data[count];
	for (unsigned int i=0; i < count; i++){
		data[i].rollno = 0;
		data[i].present = 0;
		data[i].absent = 0;
	}

	manipulate(data_in, &count, data);

	generate(data, count, out_l, out_g);
}

int main(){
	char filename[] = "database_12jan2017.csv";
	char out_l[] = "L75.csv";
	char out_g[] = "G75.csv";
	database(filename, out_l, out_g);

	return 0;
}

/* Created by Ayush Sharma. Signed as AShar.*/
