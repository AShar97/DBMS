#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>

#define MAX_STRING 50

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

void read_course_credits(){
	char filename[] = "database-19-jan-2018/database-19-jan-2018/course-credits.csv";
	unsigned int count = file_lines(filename);

	char sqlfile[] = "150123046_cc.sql";

	FILE *fp, *fw;
	fp = fopen(filename, "r");
	fw = fopen(sqlfile, "w+");
 
	// Extract data from file , store in temp variables and write in file

	char course[MAX_STRING] = {'\0'};
	unsigned int credits = 0;

	for (unsigned int i=0; i<count; i++){
		fscanf(fp, " %[^,],%u", course, &credits);
		fprintf(fw, "INSERT INTO cc (course_id, number_of_credits) VALUES (\'%s\', %u);\n", course, credits);
		// fprintf(fw, "INSERT INTO cc_temp (course_id, number_of_credits) VALUES (\'%s\', %u);\n", course, credits);
		// fprintf(fw, "INSERT INTO cc_clone (course_id, number_of_credits) VALUES (\'%s\', %u);\n", course, credits);
	}
 
	// Close the file
	fclose(fp);
	fclose(fw);

}

void read_exam_date_time(){
	char filename[] = "database-19-jan-2018/database-19-jan-2018/exam-time-table.csv";
	unsigned int count = file_lines(filename);

	char sqlfile[] = "150123046_ett.sql";

	FILE *fp, *fw;
	fp = fopen(filename, "r");
	fw = fopen(sqlfile, "w+");
 
	
	// Extract data from file , store in temp variables and write in file

	unsigned int a = 0, b = 0, c = 0;
	char course[MAX_STRING] = {'\0'}, date[MAX_STRING] = {'\0'}, stime[MAX_STRING] = {'\0'}, etime[MAX_STRING] = {'\0'};


	for (unsigned int i=0; i<count; i++){
		fscanf(fp, " %[^,],%[^,],%[^,],%[^\n]", course, date, stime, etime);
		fprintf(fw, "INSERT INTO ett (line_number, course_id, exam_date, start_time, end_time) VALUES (%u, \'%s\', \'%s\', \'%s\', \'%s\');\n", i+1, course, date, stime, etime);
		// fprintf(fw, "INSERT INTO ett_temp (course_id, exam_date, start_time, end_time) VALUES (\'%s\', \'%s\', \'%s\', \'%s\');\n", course, date, stime, etime);
		// fprintf(fw, "INSERT INTO ett_clone (course_id, exam_date, start_time, end_time) VALUES (\'%s\', \'%s\', \'%s\', \'%s\');\n", course, date, stime, etime);
	}
 
	// Close the file
	fclose(fp);
	fclose(fw);

}

unsigned int number_courses(char* directory){
	unsigned int number = 0;

	size_t path_len = strlen(directory);
	char *buf;
	size_t len;

	DIR *d = opendir(directory);
	struct dirent *p;

	if (d == NULL) {
		printf("Cannot open directory %s\n", directory);
		return 0;
	}

	DIR * dir; struct dirent *pdir;

	while ((p = readdir(d)) != NULL) {
		if ((strcmp(p->d_name,"..")!=0) && (strcmp(p->d_name,".")!=0) && (strcmp(p->d_name,".DS_Store")!=0))
		{
			len = path_len + strlen(p->d_name) + 2;

			buf = malloc(len);

			snprintf(buf, len, "%s/%s", directory, p->d_name);

			dir = opendir(buf);
			while ((pdir = readdir(dir)) != NULL) {
				if ((strcmp(pdir->d_name,"..")!=0) && (strcmp(pdir->d_name,".")!=0) && (strcmp(pdir->d_name,".DS_Store")!=0)){
					number++;

					//printf ("%s %lu\n", pdir->d_name, strlen((pdir->d_name)));
				}
			}
			free(buf);
		}
	}
	return number;
}

void read_course_stud(char* filename, char course[MAX_STRING]){
	unsigned int count = file_lines(filename);

	FILE *fp, *fw, *csv;
	fp = fopen(filename, "r");

	char sqlfile[] = "150123046_cwsl.sql";

	fw = fopen(sqlfile, "a+");

	char csvfile[] = "cwsl.csv";
	csv = fopen(csvfile, "a+");
 
	// Extract data from file , store in temp variables and write in file

	unsigned int number = 0;
	char rollno[MAX_STRING] = {'\0'}, name[MAX_STRING] = {'\0'}, email[MAX_STRING] = {'\0'};

	for (unsigned int i=0; i<count; i++){
		fscanf(fp, " %u,%[^,],%[^,],%[^\n]", &number, rollno, name, email);
		fprintf(fw, "INSERT INTO cwsl (course_id, serial_number, roll_number, name, email) VALUES (\'%s\', %u, \'%s\', \'%s\', \'%s\');\n", course, number, rollno, name, email);
		// fprintf(fw, "INSERT INTO cwsl_temp (cid, serial_number, roll_number, name, email) VALUES (\'%s\', %u, \'%s\', \'%s\', \'%s\');\n", course, number, rollno, name, email);
		// fprintf(fw, "INSERT INTO cwsl_clone (cid, serial_number, roll_number, name, email) VALUES (\'%s\', %u, \'%s\', \'%s\', \'%s\');\n", course, number, rollno, name, email);
		fprintf(csv, "%u, %s, %s, %s, %s\n", number, rollno, name, email, course);
	}
 
	// Close the file
	fclose(fp);
	fclose(fw);
	fclose(csv);

}

void course_stud_list(){

	char directory[] = "database-19-jan-2018/database-19-jan-2018/course-wise-students-list";
	
	size_t path_len = strlen(directory);
	char *buf;
	size_t len;

	char * course_name, * dot;
	size_t course_name_len;

	char *filename_buf;
	size_t filename_len;

	DIR *d = opendir(directory);
	struct dirent *p;

	DIR * dir; struct dirent *pdir;

	while ((p = readdir(d)) != NULL) {
		if ((strcmp(p->d_name,"..")!=0) && (strcmp(p->d_name,".")!=0) && (strcmp(p->d_name,".DS_Store")!=0))
		{
			len = path_len + strlen(p->d_name) + 2;

			buf = malloc(len);

			snprintf(buf, len, "%s/%s", directory, p->d_name);

			dir = opendir(buf);
			while ((pdir = readdir(dir)) != NULL) {
				if ((strcmp(pdir->d_name,"..")!=0) && (strcmp(pdir->d_name,".")!=0) && (strcmp(pdir->d_name,".DS_Store")!=0)){
					
					dot = strchr(pdir->d_name, '.');
					course_name_len = (dot - (pdir->d_name));
					course_name = malloc(course_name_len + 1);

					strncpy(course_name, (pdir->d_name), course_name_len);

					filename_len = len + strlen(pdir->d_name) + 2;

					filename_buf = malloc(filename_len);

					snprintf(filename_buf, filename_len, "%s/%s", buf, pdir->d_name);

					read_course_stud(filename_buf, course_name);
				}
			}

			free(buf);
			free(course_name);
			free(filename_buf);
		}
	}
}

int main(){
	read_course_credits();
	read_exam_date_time();
	course_stud_list();
	return 0;
}
