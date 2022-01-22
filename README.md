

# Compute OP for your mutant reduction strategy

This .md shows the main steps to compute OP to evaluate a mutation reduction strategy in "Mutant reduction evaluation: what is there and what is missing?"

## Step 1: Run mutation testing

* For a project (e.g. the project in [`project/project.rar/`](https://github.com/zhangpengNJU/MutantReductionEvaluation/tree/main/project)), please modify the "pom.xml" to make sure the PIT plugin is used correctly.
* For example, if you have installed PIT-HOM at local, you can implement high-order mutation testing according to the following configuration:

```xml
        <plugin>
            <groupId>org.pitest</groupId>
            <artifactId>pitest-parent</artifactId>
	        <version>1.4.8-HOM</version>
        </plugin>
```
* After modifing the "pom.xml", you can run mutation testing to obtain the report. For example, by command line, you can use:
```
mvn org.pitest:pitest-maven:mutationCoverage -DoutputFormats=XML -DfullMutationMatrix=true
```
* Some example reports are in [`PITreports`](https://github.com/zhangpengNJU/MutantReductionEvaluation/tree/main/PITreports).


## Step 2: Get the kill relationship matrix

By resolving the pit report, the kill relationship between all mutants and all test cases can be obtained.

## Step 3: Mutant redution

Use the strategy you want to evaluate to select mutants.

* You should resolve the PIT report by your script to obtain the wanted information in Setp 2 & 3. 
* An example information CSV is attached in [`coverage`](https://github.com/zhangpengNJU/MutantReductionEvaluation/tree/main/coverage). In a CSV, for a mutant, we record the line number, label(kill or not), mutator, kill tests(sometimes too long to record), path and the coverage information(by cobertura).

## Step 4: Compute OP
The script OP.py in [`code`](https://github.com/zhangpengNJU/MutantReductionEvaluation/tree/main/code) provides the functions to compute OP and EROP. To use it, you should obtain the matrix and the selected mutants' index first. In the script, we use the random mutant selection as the example. 


## Contact us

Mail: dz1833034@smail.nju.edu.cn
