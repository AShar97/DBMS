#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>

#define MAX_STRING 50
#define STUD_MAX 1000
#define REG_MAX 20
#define EXAM_MAX 5
#define COURSE_MAX 500
#define ALL_STUD 50000

int cmptillwhite(char a[MAX_STRING], char b[MAX_STRING]){
	for (int i = 0; i < MAX_STRING; ++i){
		if ((a[i]=='\0' || a[i]=='\n' || a[i]==' ') && (b[i]=='\0' || b[i]=='\n' || b[i]==' ')){
			return 0;
		}

		if ((a[i]=='\0' || a[i]=='\n' || a[i]==' ') || (b[i]=='\0' || b[i]=='\n' || b[i]==' ')){
			return 1;
		}

		if ((a[i] != b[i])){
			return -1;
		}
	}
	return 3;
}

struct course_credits{
	char course[MAX_STRING];
	unsigned int credits;
};

struct exam_date_time{
	char course[MAX_STRING];
	unsigned int date_time;
};

struct course_list_elem{
	char course[MAX_STRING];
	char rollno_list[STUD_MAX][MAX_STRING];
	char names[STUD_MAX][MAX_STRING];
	unsigned int rollno_list_length;
};

//struct course_list_all{
//	struct course_list_elem * course_stud;
//	unsigned int course_list_length;
//};

//SP Saheb Zindabad.
struct student{
	char roll_no[MAX_STRING];
	char name[MAX_STRING];
	char courses[REG_MAX][MAX_STRING];
	unsigned int exams[REG_MAX][EXAM_MAX];
	unsigned int coursenum;
	unsigned int examnum[REG_MAX];
	unsigned int totalcredits;
};

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

struct course_credits * read_course_credits(char * filename){
	unsigned int count = file_lines(filename);

	struct course_credits * course_credits_list = (struct course_credits *) malloc(sizeof(struct course_credits) * count);

	for (unsigned int i=0; i<count; i++){
		course_credits_list[i].credits = 0;
		//(course_credits_list[i].course)[0] = '\0';
		for (unsigned int j = 0; j < MAX_STRING; ++j)
		{
			(course_credits_list[i].course)[j] = '\0';
		}
		
	}

	FILE *fp;
	fp = fopen(filename, "r");
 
	// Check if file exists
	if (fp == NULL)
	{
		printf("Could not open file %s", filename);
		return 0;
	}
	
	// Extract data from file= and store in data_in
	for (unsigned int i=0; i<count; i++){
		//fscanf(fp, "%[^,]s", (course_credits_list[i].course));
		//fscanf(fp, "%*c%u", &(course_credits_list[i].credits));
		fscanf(fp, " %[^,],%u", (course_credits_list[i].course), &(course_credits_list[i].credits));
	}
 
	// Close the file
	fclose(fp);

	//qsort((void*)data_in, count, sizeof(data_in[0]), comparator);

	return(course_credits_list);
}

struct exam_date_time * read_exam_date_time(char * filename){
	unsigned int count = file_lines(filename);

	struct exam_date_time * exam_date_time_list = (struct exam_date_time *) malloc(sizeof(struct exam_date_time) * count);

	for (unsigned int i=0; i<count; i++){
		exam_date_time_list[i].date_time = 0;
		//(exam_date_time_list[i].course)[0] = '\0';
		for (int j = 0; j < MAX_STRING; ++j)
		{
			(exam_date_time_list[i].course)[j] = '\0';
		}
	}

	FILE *fp;
	fp = fopen(filename, "r");
 
	// Check if file exists
	if (fp == NULL)
	{
		printf("Could not open file %s", filename);
		return 0;
	}
	unsigned int a = 0, b = 0, c = 0;
	// Extract data from file= and store in data_in
	for (unsigned int i=0; i<count; i++){
		a = 0; b = 0; c = 0;

		//fscanf(fp, "%[^,]s%u", (course_credits_list[i].course), &(course_credits_list[i].credits));
		//fscanf(fp, "%[^,]s", (exam_date_time_list[i].course));
		//fscanf(fp, "%*c%*u%*c%u%*c%u%*c%u%*s", &a, &b, &c);
		fscanf(fp, " %[^,],%*u-%u-%u,%u%*[^\n]", (exam_date_time_list[i].course), &a, &b, &c);
		exam_date_time_list[i].date_time = a*10000 + b*100 + c;

	}
 
	// Close the file
	fclose(fp);

	//qsort((void*)data_in, count, sizeof(data_in[0]), comparator);

	return(exam_date_time_list);
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

int read_course_stud(char* filename, unsigned int length, char rollno_list[STUD_MAX][MAX_STRING], char names[STUD_MAX][MAX_STRING]){
	FILE *fp;
	fp = fopen(filename, "r");
 
	// Check if file exists
	if (fp == NULL)
	{
		printf("Could not open file %s", filename);
		return 0;
	}
	
	// Extract data from file and store in data_in
	for (unsigned int i=0; i<length; i++){
		fscanf(fp, " %*u,%[^,],%[^,]%*[^\n]", &(rollno_list[i][0]), &(names[i][0]));
		//" %d,%[^,],%[^,],%[^\n]"
		//fscanf(fp, " %*u,%[^,],%*[^,]%*[^\n]", &(rollno_list[i][0]));//, &(names[i][0]));
		
	}
 
	// Close the file
	fclose(fp);

	//qsort((void*)data_in, count, sizeof(data_in[0]), comparator);

	return 1;
}

struct course_list_elem * course_stud_list(char* directory, unsigned int course_list_length){
	
	struct course_list_elem * course_list = (struct course_list_elem *) malloc(sizeof(struct course_list_elem) * course_list_length);

	unsigned int number = 0;


	for (unsigned int i=0; i<course_list_length; i++){
		course_list[i].rollno_list_length = 0;
		//(course_list[i].course)[0] = '\0';
		//(course_list[i].rollno_list)[0][0] = '\0';
		//(course_list[i].names)[0][0] = '\0';
		for (int j = 0; j < MAX_STRING; ++j)
		{
			(course_list[i].course)[j] = '\0';
		}
		for (int j = 0; j < STUD_MAX; ++j)
		{
			for (int k = 0; k < MAX_STRING; ++k)
			{
				(course_list[i].rollno_list)[j][k] = '\0';
				(course_list[i].names)[k][j] = '\0';
			}
		}
	}

	size_t path_len = strlen(directory);
	char *buf;
	size_t len;

	char * course_name, * dot;
	size_t course_name_len;

	char *filename_buf;
	size_t filename_len;

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

			//printf("%s\n", buf);

			dir = opendir(buf);
			while ((pdir = readdir(dir)) != NULL) {
				if ((strcmp(pdir->d_name,"..")!=0) && (strcmp(pdir->d_name,".")!=0) && (strcmp(pdir->d_name,".DS_Store")!=0)){
					
					dot = strchr(pdir->d_name, '.');
					course_name_len = (dot - (pdir->d_name));
					course_name = malloc(course_name_len + 1);

					//memcpy(course_name, (pdir->d_name), course_name_len);
					strncpy(course_name, (pdir->d_name), course_name_len);

					//course_name_len = strlen(pdir->d_name)-4;
					//course_name = malloc(strlen(pdir->d_name));

					//memcpy(course_name, (pdir->d_name), course_name_len);


					filename_len = len + strlen(pdir->d_name) + 2;

					filename_buf = malloc(filename_len);

					snprintf(filename_buf, filename_len, "%s/%s", buf, pdir->d_name);



					course_list[number].rollno_list_length = file_lines(filename_buf);

					//memcpy(course_list[number].course, course_name, course_name_len);
					strcpy(course_list[number].course, course_name);

					//printf("%s\n", filename_buf);

					read_course_stud(filename_buf, course_list[number].rollno_list_length, course_list[number].rollno_list, course_list[number].names);

					//printf("%s %s\n", course_list[number].rollno_list[0], course_list[number].rollno_list[1]);

					//printf("%s %s\n", course_list[number].names[0], course_list[number].names[1]);

					number++;

					//printf ("%s %lu\t", pdir->d_name, strlen((pdir->d_name)));

					//printf("%s %s\n", course_name, filename_buf);
				}
			}

			free(buf);
			free(course_name);
			free(filename_buf);
		}
	}
	
	return course_list;
}

void getcredits(struct course_credits * course_credits_list, unsigned int course_credits_list_length,
				char course[MAX_STRING], unsigned int * totalcredits
				){
	for (unsigned int i = 0; i < course_credits_list_length; ++i)
	{
		//if (cmptillwhite(course, course_credits_list[i].course) == 0)
		if (strcmp(course, course_credits_list[i].course) == 0)
		{
			*totalcredits += course_credits_list[i].credits;
		}
	}
}

void add_exams(	unsigned int exams[REG_MAX][EXAM_MAX], unsigned int examnum[REG_MAX],
				char course[MAX_STRING], unsigned int coursenum,
				struct exam_date_time * exam_date_time_list, unsigned int count
				)
{
	for (unsigned int i = 0; i < count; ++i)
	{
		//if (cmptillwhite(course, exam_date_time_list[i].course) == 0)
		if (strcmp(course, exam_date_time_list[i].course) == 0)
		{
			exams[coursenum][examnum[coursenum]] = exam_date_time_list[i].date_time;
			examnum[coursenum]++;
		}
	}
}

struct student * stud_table(struct course_list_elem * course_list, unsigned int course_list_length,
							struct course_credits * course_credits_list, unsigned int course_credits_list_length,
							struct exam_date_time * exam_date_time_list, unsigned int exam_date_time_list_length,
							unsigned int * stud_num
							)
{
	struct student * all_stud_table = (struct student *) malloc(sizeof(struct student) * ALL_STUD);

	for (unsigned int i = 0; i < ALL_STUD; ++i){
		all_stud_table[i].coursenum = 0;	all_stud_table[i].totalcredits = 0;
		//(all_stud_table[i].examnum)[0] = 0;
		//(all_stud_table[i].courses)[0][0] = '\0';	(all_stud_table[i].exams)[0][0] = 0;
		//(all_stud_table[i].roll_no)[0] = '\0';	(all_stud_table[i].name)[0] = '\0';
		for (int j = 0; j < REG_MAX; ++j)
		{
			(all_stud_table[i].examnum)[j] = 0;

			for (int k = 0; k < MAX_STRING; ++k)
			{
				(all_stud_table[i].courses)[j][k] = '\0';
			}

			for (int k = 0; k < EXAM_MAX; ++k)
			{
				(all_stud_table[i].exams)[j][k] = 0;
			}
		}

		for (int j = 0; j < MAX_STRING; ++j)
		{
			(all_stud_table[i].name)[j] = '\0';
			(all_stud_table[i].roll_no)[j] = '\0';
		}

	}

	unsigned int number = 0, k=0;

	for (unsigned int i = 0; i < course_list_length; ++i){

		for (unsigned int j = 0; j < course_list[i].rollno_list_length; ++j){

			k = 0;
			while(k<number && strcmp(((course_list[i]).rollno_list[j]), ((all_stud_table[k]).roll_no))!=0){
			//while(k<number && cmptillwhite(((course_list[i]).rollno_list[j]), ((all_stud_table[k]).roll_no))!=0){
				k++;
			}

			if(k == number){
				number++;
			}
			

			if (all_stud_table[k].coursenum == 0)
			{
				//memcpy(all_stud_table[k].roll_no, course_list[i].rollno_list[j], strlen(course_list[i].rollno_list[j]));
				//memcpy(all_stud_table[k].name, course_list[i].names[j], strlen(course_list[i].names[j]));
				strcpy(all_stud_table[k].roll_no, course_list[i].rollno_list[j]);
				strcpy(all_stud_table[k].name, course_list[i].names[j]);
			}

			getcredits(course_credits_list, course_credits_list_length, course_list[i].course, &(all_stud_table[k].totalcredits));

			//memcpy((all_stud_table[k].courses)[all_stud_table[k].coursenum], course_list[i].course, strlen(course_list[i].course));
			strcpy((all_stud_table[k].courses)[all_stud_table[k].coursenum], course_list[i].course);

			add_exams(	all_stud_table[k].exams, all_stud_table[k].examnum,
						course_list[i].course, all_stud_table[k].coursenum,
						exam_date_time_list, exam_date_time_list_length
						);
			
			all_stud_table[k].coursenum++;
			
		}
		
	}

	*stud_num = number;
	return(all_stud_table);
}

_Bool check_not_done(char clash1[REG_MAX][MAX_STRING], char clash2[REG_MAX][MAX_STRING], unsigned short int clash_count,
				char str1[MAX_STRING], char str2[MAX_STRING]){
	for (unsigned short int i =0; i < clash_count; i++){
		if((strcmp(clash1[i],str1)==0 && strcmp(clash2[i],str2)==0) || (strcmp(clash1[i],str2)==0 && strcmp(clash2[i],str1)==0)){
			return 0;
		}
	}
	return 1;
}

void check_exam_clash(struct student* all_stud_table, unsigned int stud_num){
	FILE *fp = fopen("exam-clash.csv", "w+");

	char clash1[REG_MAX][MAX_STRING] = {'\0'};
	char clash2[REG_MAX][MAX_STRING] = {'\0'};
	unsigned short int clash_count = 0;

	unsigned int totalcount = 0;

	printf("Checking Exam Clashes.\n");
	for (unsigned int i = 0; i < stud_num; ++i)
	{
		for (unsigned int j = 0; j < all_stud_table[i].coursenum; ++j)
		{
			for (unsigned int k = 0; k < all_stud_table[i].examnum[j]; ++k)
			{
				for (unsigned int l = j+1; l < all_stud_table[i].coursenum; ++l)
				{
					for (unsigned int m = 0; m < all_stud_table[i].examnum[l]; m++)
					{
						if (all_stud_table[i].exams[j][k] == all_stud_table[i].exams[l][m])
						{
							if (check_not_done(clash1, clash2, clash_count, all_stud_table[i].courses[j], all_stud_table[i].courses[l]))
							{
								totalcount++;

								strcpy(clash1[clash_count], all_stud_table[i].courses[j]);
								strcpy(clash2[clash_count++], all_stud_table[i].courses[l]);

								//printf("%s\t%s\t%s-%s clashes exam.\n",
								//		all_stud_table[i].roll_no, all_stud_table[i].name,
								//		all_stud_table[i].courses[j], all_stud_table[i].courses[l]);

								fprintf(fp, "%s,%s,%s,%s\n",
										all_stud_table[i].roll_no, all_stud_table[i].name,
										all_stud_table[i].courses[j], all_stud_table[i].courses[l]);
							}
						}
					}
				}
			}
			
		}
	}

	fclose(fp);

	printf("Total %u Exam Clashes.\n", totalcount);
}
	
void check_credits(struct student* all_stud_table, unsigned int stud_num){
	FILE *fp = fopen("credits-clash.csv", "w+");

	printf("Checking Credits Constraint.\n");
	unsigned int totalcount = 0;
	for (unsigned int i = 0; i < stud_num; ++i)
	{
		if (all_stud_table[i].totalcredits > 40)
		{
			totalcount++;
			//printf("%s\t%s\t\t\t%u Credits - Constraint limit exceeding.\n",
			//		all_stud_table[i].roll_no, all_stud_table[i].name,
			//		all_stud_table[i].totalcredits);

			fprintf(fp, "%s,%s,%u\n",
					all_stud_table[i].roll_no, all_stud_table[i].name,
					all_stud_table[i].totalcredits);
		}
	}

	fclose(fp);

	printf("Total %u Credits-Constraint Clashes.\n", totalcount);
}


int main(){
	char directory[] = "database-19-jan-2018/course-wise-students-list";
	char filename1[] = "database-19-jan-2018/course-credits.csv";
	char filename2[] = "database-19-jan-2018/exam-time-table.csv";

	unsigned int course_credits_list_length = file_lines(filename1);
	struct course_credits * course_credits_list = read_course_credits(filename1);

	unsigned int exam_date_time_list_length = file_lines(filename2);
	struct exam_date_time * exam_date_time_list = read_exam_date_time(filename2);

	unsigned int course_list_length = number_courses(directory);
	//printf("%u\n", course_list_length);

	struct course_list_elem * course_list = course_stud_list(directory, course_list_length);

	unsigned int stud_num = 0;

	struct student* all_stud_table = stud_table(course_list, course_list_length,
												course_credits_list, course_credits_list_length,
												exam_date_time_list, exam_date_time_list_length,
												&stud_num
												);
	
	check_credits(all_stud_table, stud_num);
	
	check_exam_clash(all_stud_table, stud_num);

/*
	//getcredits(course_credits_list, course_credits_list_length, "MA101");
	{//test of Course-Credit data Correct
		FILE *fp;
		
		// Open the file
		fp = fopen("out_course-credit.csv", "w+");
	 
		// Check if file exists
		if (fp == NULL)
		{
			printf("Could not open file %s", "out_course-credit.csv");
			return 0;
		}


		unsigned int count = course_list_length;
		for (unsigned int i=0; i<count; i++){
			//printf("%s %s\n", course_list[i].rollno_list[0], course_list[i].rollno_list[1]);

			fprintf(fp, "%s,%u\n", course_list[i].course, getcredits(course_credits_list, course_credits_list_length, course_list[i].course));

			//for (unsigned int j = 0; j < course_list[i].rollno_list_length; ++j){
			//for (unsigned int j = 0; j < (course_list[i]).rollno_list_length; ++j){
				//fprintf(fp, ",%s", ((course_list[i]).rollno_list[j]));

				//printf("%s %u", course_credits_list[i].course, course_credits_list[i].credits);
				
				//printf("%s %u", exam_date_time_list[i].course, exam_date_time_list[i].date_time);
			//}
			//fprintf(fp, "\n");
			//for (unsigned int j = 0; j < (course_list[i]).rollno_list_length; ++j){
				//fprintf(fp, ",%s", ((course_list[i]).names[j]));

				//printf("%s %u", course_credits_list[i].course, course_credits_list[i].credits);
				
				//printf("%s %u", exam_date_time_list[i].course, exam_date_time_list[i].date_time);
			//}
			//fprintf(fp, "\n");
		}
	 
		// Close the file
		fclose(fp);
	}
*/


/*
	{//test of Course data Correct
		FILE *fp;
		
		// Open the file
		fp = fopen("out_course.csv", "w+");
	 
		// Check if file exists
		if (fp == NULL)
		{
			printf("Could not open file %s", "out_course.csv");
			return 0;
		}


		unsigned int count = course_list_length;
		for (unsigned int i=0; i<count; i++){
			//printf("%s %s\n", course_list[i].rollno_list[0], course_list[i].rollno_list[1]);

			fprintf(fp, "%s ", course_list[i].course);

			//for (unsigned int j = 0; j < course_list[i].rollno_list_length; ++j){
			for (unsigned int j = 0; j < (course_list[i]).rollno_list_length; ++j){
				fprintf(fp, ",%s", ((course_list[i]).rollno_list[j]));

				//printf("%s %u", course_credits_list[i].course, course_credits_list[i].credits);
				
				//printf("%s %u", exam_date_time_list[i].course, exam_date_time_list[i].date_time);
			}
			fprintf(fp, "\n");
			for (unsigned int j = 0; j < (course_list[i]).rollno_list_length; ++j){
				fprintf(fp, ",%s", ((course_list[i]).names[j]));

				//printf("%s %u", course_credits_list[i].course, course_credits_list[i].credits);
				
				//printf("%s %u", exam_date_time_list[i].course, exam_date_time_list[i].date_time);
			}
			fprintf(fp, "\n");
		}
	 
		// Close the file
		fclose(fp);
	}
*/

/*
	{//test of Stud data Correct
		FILE *fp;
		
		// Open the file
		fp = fopen("out_stud.csv", "w+");
	 
		// Check if file exists
		if (fp == NULL)
		{
			printf("Could not open file %s", "out_stud.csv");
			return 0;
		}


		unsigned int count = stud_num;
		printf("%u\n", stud_num);
		for (unsigned int i=0; i<count; i++){
			fprintf(fp, "%s,%s,", all_stud_table[i].roll_no, all_stud_table[i].name);

			for (unsigned int j = 0; j < all_stud_table[i].coursenum; ++j){
				fprintf(fp, "%s,,,", ((all_stud_table[i]).courses[j]));
			}
			fprintf(fp, "\n");
			for (unsigned int j = 0; j < all_stud_table[i].coursenum; ++j){
				for (unsigned int k = 0; k < all_stud_table[i].examnum[j]; ++k)
				{
					fprintf(fp, ",%u", ((all_stud_table[i]).exams[j][k]));
				}
			}
			fprintf(fp, "\n%u\n", all_stud_table[i].totalcredits);
		}
	 
		// Close the file
		fclose(fp);
	}
*/


/*
{
	DIR *d = opendir(directory);
	struct dirent *p;

	if (d == NULL) {
		printf("Cannot open directory %s\n", directory);
		return 0;
	}

	while ((p = readdir(d)) != NULL) {
		if ((strcmp(p->d_name,"..")!=0) && (strcmp(p->d_name,".")!=0) && (strcmp(p->d_name,".DS_Store")!=0))
		{
			printf ("%s\n", p->d_name);
		}
	}
}
*/

/*
	{//test
	unsigned int count = course_list_length;
	for (unsigned int i=0; i<count; i++){
		//printf("%s %s\n", course_list[i].rollno_list[0], course_list[i].rollno_list[1]);

		printf("%s\t- ", course_list[i].course);

		//for (unsigned int j = 0; j < course_list[i].rollno_list_length; ++j){
		for (unsigned int j = 0; j < 5; ++j){
			printf("%s ", ((course_list[i]).rollno_list[j]));

			//printf("%s %u", course_credits_list[i].course, course_credits_list[i].credits);
			
			//printf("%s %u", exam_date_time_list[i].course, exam_date_time_list[i].date_time);
		}
		printf("\n");
	}

	//printf("\n\n%u\n\n%u\n", count, exam_date_time_list_length);
	
	}
*/

/*
	{//test
	//unsigned int count = file_lines(filename1);
	unsigned int count = course_credits_list_length;
	for (unsigned int i=0; i<count; i++){
		printf("%s %u", course_credits_list[i].course, course_credits_list[i].credits);
		
		//printf("%s %u", exam_date_time_list[i].course, exam_date_time_list[i].date_time);
	
	}

	//printf("\n\n%u\n\n%u\n", count, exam_date_time_list_length);
	
	}
*/

	return 0;
}

/* Created by Ayush Sharma. Signed as AShar.*/
