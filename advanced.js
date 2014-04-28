function Course(crn, time, days, type) {
    this.crn = crn
    this.time = time
    this.days = days
    this.type = type
}

var a = new Course(1, "10:00 AM - 10:50 AM", "MWF", "Lec")
var b = new Course(2, "01:00 PM - 01:50 PM\n02:00 PM - 02:50 PM", "M\nM", "Discussion/Recitation\nLaboratory")
var c = new Course(3, "02:00 PM - 02:50 PM\n03:00 PM - 03:50 PM", "M\nM", "Discussion/Recitation\nLaboratory")
var courses = []
courses.push(a)
courses.push(b)
courses.push(c)
permutate(courses)

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
    var results = type[Object.keys(type)[0]]
    for (var j = 1; j < Object.keys(type).length; ++j)
    {
        //reset list to empty
        var tempSoln = []
        for(var l = 0; l < type[Object.keys(type)[j]].length; ++l)
        {
            tempSoln.push(genPermutation(results, [type[Object.keys(type)[j]][l] ]))
        }
        // swap out list with permutated list
        results = tempSoln
    }
    return results
    // check and see if these permuataions intersect with schedule
}

/*
 soln is a list of permutations to try to add an elem to
 elem is an element(s) to add
 */
function genPermutation(soln, elem){
    var permutations = []
    if (soln.length == 0)
    {
        return elem
    }
    if (elem.length == 0)
    {
        return soln
    }
    for (var i = 0; i < soln.length; ++i)
    {
        for (var j = 0; j < elem.length; ++j)
        {
            if (!timeConflict([soln[i]], elem[j]))
            {
                console.log(soln[i])
                console.log(elem[j])

                permutations.push([soln[i]].push(elem[j]))
                console.log(permutations)
            }
        }
    }
    return permutations
}


/*
 [event1, event2...], event
 List is a list of events known to not have conflicts
 elem is a event to check if we have a time conflict or not
 one crn might have more than 1 slot (block classes/schedules)
 */
function timeConflict(List, elem){
    if (List.length == 0)
    {
        return false
    }
    var elemDays = elem.days.split("\n")
    var elemTime = elem.time.split("\n")
    for (var i = 0; i < elemDays.length; ++i)
    {
        if (elemDays[i] != "n.a." && elemTime[i] != "ARRANGED")
        {
            for (var j = 0; j < List.length; ++j)
            {
                var listDays = List[j].days.split("\n")
                var listTime = List[j].time.split("\n")
                for (var k = 0; k < listDays.length; ++k)
                {
                    if (listDays[k] != "n.a." && listTime[k] != "ARRANGED")
                    {
                        if (isSameDays(elemDays[i], listDays[k]))
                        {
                            if (isSameTime(elemTime[i], listTime[k]))
                            {
                                return true
                            }
                        }
                    }
                }
            }
        }
    }
    return false
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

    if (haystackStartTime < needleStartTime && needleStartTime < haystackEndTime){
        return true;
    }
    else {
        return haystackStartTime < needleEndTime && needleEndTime < haystackEndTime;
    }
//    haystackStartTime < needleStartTime < needleEndTime < haystackEndTime
}