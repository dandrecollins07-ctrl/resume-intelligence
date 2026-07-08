const Lookup = {
    low: "bg-red-500 text-white",
    medium: "bg-yellow-500 text-white",
    high: "bg-green-500 text-white"
}

function getScoreColor(percent) {
    if (percent < 40) {
        return Lookup.low
    }
    else if (percent <= 70) {
        return Lookup.medium
    }
    else {
        return Lookup.high
    }
}

export { Lookup, getScoreColor };