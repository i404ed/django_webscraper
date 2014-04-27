/*
CorseList is the list of sections available for 1 CourseID
*/
/*
needs list of slots/courses
[course1,course2]
*/
function permutate(CourseList) {
	// finds out different types and split into bins
	var type = {}
	for (var i=0; i<CourseList.length; i++)
	{ 
		var Course = CourseList[i]
		if (!(Course.type in type))
		{
	    type[Course.type] = []
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
[event1, event2...], event
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
		return true
	}
	for (var i = 0; i < List.length; ++i)
	{
		if (List[i].days == "n.a." || List[i].time == "ARRANGED") 
		{
			// do nothing, check next event
		}
		else
		{
			if (isSameDays(elem.days, List[i].days))
			{
				if (isSameTime(elem.time, List[i].time))
				{

				}
			}
		}
		// List[i] = event
		// elem = event
	}
}

/*
Needs string format
"MTWRF"
needle, the days to check
haystack, the days to check against
if any of needle is in haystack, returns true
*/
function isSameDays(needleStr, haystackStr){
    var needle = needleStr.split("")
    var haystack = haystackStr.split("")
	for (var i = 0; i < needle.length; ++i)
	{
		if (haystack.indexOf(needle[i]) > -1)
		{
			return true
		}
	}
	return false
}
/*
needs times as strings
"02:00 PM - 03:50 PM"
[1]:[2] [3] - [4]:[5] [6]
/^ *(\d+):(\d+) *(AM|PM) *- *(\d+):(\d+) *(AM|PM)/i
*/
function isSameTime(needleStr, haystackStr){
    //match using regex
    var needleRegex = needleStr.match(/^ *(\d+):(\d+) *(AM|PM) *- *(\d+):(\d+) *(AM|PM)/i)
    var haystackRegex = haystackStr.match(/^ *(\d+):(\d+) *(AM|PM) *- *(\d+):(\d+) *(AM|PM)/i)
    //+12 if pm
    if (needleRegex[3].match(/PM/i))
    {
        needleRegex[1] = parseInt(needleRegex[1]) + 12
    }
    if (needleRegex[6].match(/PM/i))
    {
        needleRegex[4] = parseInt(needleRegex[4]) + 12
    }
    //make date time obj and set
    var needleStartTime = new Date()
    var needleEndTime = new Date()
    needleStartTime.setHours(needleRegex[1] , needleRegex[2], 00, 00)
    needleEndTime.setHours(needleRegex[4] , needleRegex[5], 00, 00)
    //+12 if pm
    if (haystackRegex[3].match(/PM/i))
    {
        haystackRegex[1] = parseInt(haystackRegex[1]) + 12
    }
    if (haystackRegex[6].match(/PM/i))
    {
        haystackRegex[4] = parseInt(haystackRegex[4]) + 12
    }
    //make date time obj and set
    var haystackStartTime = new Date()
    var haystackEndTime = new Date()
    haystackStartTime.setHours(haystackRegex[1] , haystackRegex[2], 00, 00)
    haystackEndTime.setHours(haystackRegex[4] , haystackRegex[5], 00, 00)

    if (haystackStartTime < needleStartTime && needleStartTime < needleEndTime){
        return true;
    }
    else {
        return haystackStartTime < needleEndTime && needleEndTime < needleEndTime;
    }
//    haystackStartTime < needleStartTime < needleEndTime < haystackEndTime
}