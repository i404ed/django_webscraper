/*
CorseList is the list of sections available for 1 CourseID
*/
function permutate(CourseList) {
	// finds out different types and split into bins
	var type = {}
	for (var i=0; i<CourseList.length; i++)
	{ 
		var Course = CourseList[i]
		if (!(Course.type in type))
		{
	    list[Course.type] = []
		}
		type[Course.type].push(Course)
	}
	// generates permutations for each type
	var results = [[]]
	for (var i = 0; i < type.length; ++i)
	{
		results = genPermutation(results, Object.keys(type)[i])
	}
	return results
	// check and see if these permuataions intersect with schedule
}

/*
List1 is a permutation. it is list of lists of events
[[Lecture1, Discussion1], [Lecture1, Discussion2]]
List2 is a list of things to add to the permutations
[Lab1, Lab2]
*/
function genPermutation(List1, List2){
	var permutations = []
	// if (List1.length == 0) 
	// {
	// 	return [List2]
	// }
	if (List2.length == 0) 
	{
		return List1
	}
	for (var i = 0; i < List1.length; ++i)
	{
		for (var j = 0; j < List2.length; ++j)
		{
			if (timeConflict(List1[i], List2[j])) 
			{
				permutations.push(List1[i].push(List2[j]))
			}
		}
	}
	return permutations
}

/*
List is a list of events known to not have conflicts
elem is a event to check if we have a time conflict or not
*/
function timeConflict(List, elem){
	if (List.length == 0) 
	{
		return true
	}
	if (elem.days == "n.a." || elem.time == "ARRANGED") 
	{
		return true;
	}
	for (var i = 0; i < List.length; ++i)
	{
		if (List[i].days == "n.a." || List[i].time == "ARRANGED") 
		{
			// do nothing, check next event
		}
		else
		{
			var elemDays = elem.days.split("")
			var currDays = List[i].days.split("")
			if (isIn(elemDays, currDays)) 
			{
				
				if () 
				{

				}
			}
		}
		// List[i] = event
		// elem = event
	}
}

/*
needle, the list of days to check
haystack, the list of days to check against
if any of needle is in haystack, returns true
*/
function isIn(needle, haystack){
	for (var i = 0; i < needle.length; ++i)
	{
		if (haystack.indexOf(needle[i]) > -1)
		{
			return true;
		}
	}
	return false;
}