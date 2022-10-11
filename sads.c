// two parents continue to next generation
memcpy(gene[0], parent[0], sizeof(char)* beam_mat_1st);
memcpy(gene[1], parent[1], sizeof(char)* beam_mat_1st);

// crossver between the two parents (0.462 each) and mutation (0.075)
	for (int ret = 2; ret < POPULATION; ret++) {
		retry:
		for (i = 0; i < beam_mat_1st; i++) {
			seed = rand() % 1000;
			if (seed < 462) gene[ret][i] = parent[0][i];
			else if (seed > 512) gene[ret][i] = parent[1][i];
			else gene[ret][i] = rand() % 3 + '0';
		}
		// check for duplicate
		for (int cand=0; cand < ret; cand++){
			if (strcmp(gene[ret], gene[cand])==0) goto retry; 
			}
	}
