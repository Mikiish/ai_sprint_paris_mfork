void *buffer = malloc(256);

// J’écris un entier là-dedans
*(int *)buffer = 42;

// Je passe ce buffer à une fonction, qui elle pense que c’est un `char *`
process_as_string((char *)buffer);

// Je le retransforme en `MyStruct *` plus tard, sans rien dire
MyStruct *obj = (MyStruct *)buffer;