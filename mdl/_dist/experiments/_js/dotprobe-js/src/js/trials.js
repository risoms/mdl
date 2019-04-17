//for preloading
var image_array = [
'src/img/stim/i2102.jpg','src/img/stim/i2141.jpg','src/img/stim/i2205.jpg','src/img/stim/i2235.jpg','src/img/stim/i2276.jpg','src/img/stim/i2393.jpg','src/img/stim/i2397.jpg','src/img/stim/i2455.jpg','src/img/stim/i2700.jpg','src/img/stim/i2703.jpg','src/img/stim/i2745.jpg','src/img/stim/i2799.jpg','src/img/stim/i2850.jpg','src/img/stim/i2900.jpg','src/img/stim/i5390.jpg','src/img/stim/i5500.jpg','src/img/stim/i5731.jpg','src/img/stim/i7009.jpg','src/img/stim/i7041.jpg','src/img/stim/i7053.jpg','src/img/stim/i7090.jpg','src/img/stim/i7185.jpg','src/img/stim/i7493.jpg','src/img/stim/i9421.jpg','src/img/stim/i9530.jpg','src/img/stim/p0002.jpg','src/img/stim/p0006.jpg','src/img/stim/p0008.jpg','src/img/stim/p0013.jpg','src/img/stim/p0015.jpg','src/img/stim/p0021.jpg','src/img/stim/p0036.jpg','src/img/stim/p0041.jpg','src/img/stim/p0043.jpg','src/img/stim/p0047.jpg','src/img/stim/p0067.jpg','src/img/stim/p0072.jpg','src/img/stim/p0075.jpg','src/img/stim/p0076.jpg','src/img/stim/p0083.jpg','src/img/stim/p0086.jpg','src/img/stim/p0087.jpg','src/img/stim/p0092.jpg','src/img/stim/p0094.jpg','src/img/stim/p0099.jpg','src/img/stim/p0102.jpg','src/img/stim/p0110.jpg'
];

//practice stimuli
var pracBlock = [
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "ArtCube",
		"RDescription": "ArtCube",
		"LStim": "i7185.jpg",
		"RStim": "i7185.jpg",
		"Type": "iaps",
		"ID": "pi0"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "SleepMen",
		"RDescription": "SleepMen",
		"LStim": "i2397.jpg",
		"RStim": "i2397.jpg",
		"Type": "iaps",
		"ID": "pi1"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "ItalianShop",
		"RDescription": "ItalianShop",
		"LStim": "i2235.jpg",
		"RStim": "i2235.jpg",
		"Type": "iaps",
		"ID": "pi2"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "Mushroom",
		"RDescription": "Mushroom",
		"LStim": "i5500.jpg",
		"RStim": "i5500.jpg",
		"Type": "iaps",
		"ID": "pi3"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "Book",
		"RDescription": "Book",
		"LStim": "i7090.jpg",
		"RStim": "i7090.jpg",
		"Type": "iaps",
		"ID": "pi4"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "72",
		"RDescription": "72",
		"LStim": "p0072.jpg",
		"RStim": "p0072.jpg",
		"Type": "pofa",
		"ID": "pp0"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "99",
		"RDescription": "99",
		"LStim": "p0099.jpg",
		"RStim": "p0099.jpg",
		"Type": "pofa",
		"ID": "pp1"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "83",
		"RDescription": "83",
		"LStim": "p0083.jpg",
		"RStim": "p0083.jpg",
		"Type": "pofa",
		"ID": "pp2"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "41",
		"RDescription": "41",
		"LStim": "p0041.jpg",
		"RStim": "p0041.jpg",
		"Type": "pofa",
		"ID": "pp3"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "110",
		"RDescription": "110",
		"LStim": "p0110.jpg",
		"RStim": "p0110.jpg",
		"Type": "pofa",
		"ID": "pp4"
 },
	{
		"LEmotion": "Neutral",
		"REmotion": "Neutral",
		"LDescription": "6",
		"RDescription": "6",
		"LStim": "p0006.jpg",
		"RStim": "p0006.jpg",
		"Type": "pofa",
		"ID": "pp5"
}];

//pofa stimuli
var pofa =[
  {
    "id": 1,
    "Neutral": "p0021.jpg",
    "Sad": "p0015.jpg",
    "NeutralID": 21,
    "SadID": 15,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0021.jpg",
    "SadDirectory": "src/img/stim/p0015.jpg",
    "Description": "21-15",
    "Duration": 3000
  },
  {
    "id": 2,
    "Neutral": "p0047.jpg",
    "Sad": "p0043.jpg",
    "NeutralID": 47,
    "SadID": 43,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0047.jpg",
    "SadDirectory": "src/img/stim/p0043.jpg",
    "Description": "47-43",
    "Duration": 3000
  },
  {
    "id": 3,
    "Neutral": "p0072.jpg",
    "Sad": "p0067.jpg",
    "NeutralID": 72,
    "SadID": 67,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0072.jpg",
    "SadDirectory": "src/img/stim/p0067.jpg",
    "Description": "72-67",
    "Duration": 3000
  },
  {
    "id": 4,
    "Neutral": "p0110.jpg",
    "Sad": "p0102.jpg",
    "NeutralID": 110,
    "SadID": 102,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0110.jpg",
    "SadDirectory": "src/img/stim/p0102.jpg",
    "Description": "110-102",
    "Duration": 3000
  },
  {
    "id": 5,
    "Neutral": "p0083.jpg",
    "Sad": "p0075.jpg",
    "NeutralID": 83,
    "SadID": 75,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0083.jpg",
    "SadDirectory": "src/img/stim/p0075.jpg",
    "Description": "83-75",
    "Duration": 3000
  },
  {
    "id": 6,
    "Neutral": "p0099.jpg",
    "Sad": "p0094.jpg",
    "NeutralID": 99,
    "SadID": 94,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0099.jpg",
    "SadDirectory": "src/img/stim/p0094.jpg",
    "Description": "99-94",
    "Duration": 3000
  },
  {
    "id": 7,
    "Neutral": "p0041.jpg",
    "Sad": "p0036.jpg",
    "NeutralID": 41,
    "SadID": 36,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0041.jpg",
    "SadDirectory": "src/img/stim/p0036.jpg",
    "Description": "41-36",
    "Duration": 3000
  },
  {
    "id": 8,
    "Neutral": "p0092.jpg",
    "Sad": "p0087.jpg",
    "NeutralID": 92,
    "SadID": 87,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0092.jpg",
    "SadDirectory": "src/img/stim/p0087.jpg",
    "Description": "92-87",
    "Duration": 3000
  },
  {
    "id": 9,
    "Neutral": "p0006.jpg",
    "Sad": "p0002.jpg",
    "NeutralID": 6,
    "SadID": 2,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0006.jpg",
    "SadDirectory": "src/img/stim/p0002.jpg",
    "Description": "6-2",
    "Duration": 3000
  },
  {
    "id": 10,
    "Neutral": "p0013.jpg",
    "Sad": "p0008.jpg",
    "NeutralID": 13,
    "SadID": 8,
    "Type": "pofa",
    "NeutralDirectory": "src/img/stim/p0013.jpg",
    "SadDirectory": "src/img/stim/p0008.jpg",
    "Description": "13-8",
    "Duration": 3000
  }
];

//iaps stimuli
var iaps = {
	"n0": {
		"Image": "i2102.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 2102,
		"Directory": "src/img/stim/i2102.jpg",
		"Type": "iaps",
		"Description": "ManonDeck",
		"IAPSID": "n0"
	},
	"n1": {
		"Image": "i2393.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 2393,
		"Directory": "src/img/stim/i2393.jpg",
		"Type": "iaps",
		"Description": "FactoryWork",
		"IAPSID": "n1"
	},
	"n2": {
		"Image": "i2745.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 2745,
		"Directory": "src/img/stim/i2745.jpg",
		"Type": "iaps",
		"Description": "WomanGroc",
		"IAPSID": "n2"
	},
	"n3": {
		"Image": "i2850.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 2850,
		"Directory": "src/img/stim/i2850.jpg",
		"Type": "iaps",
		"Description": "LadyLookUp",
		"IAPSID": "n3"
	},
	"n4": {
		"Image": "i5390.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 5390,
		"Directory": "src/img/stim/i5390.jpg",
		"Type": "iaps",
		"Description": "RowBoats",
		"IAPSID": "n4"
	},
	"n5": {
		"Image": "i5731.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 5731,
		"Directory": "src/img/stim/i5731.jpg",
		"Type": "iaps",
		"Description": "BlueDoor",
		"IAPSID": "n5"
	},
	"n6": {
		"Image": "i7009.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 7009,
		"Directory": "src/img/stim/i7009.jpg",
		"Type": "iaps",
		"Description": "BlueMug",
		"IAPSID": "n6"
	},
	"n7": {
		"Image": "i7041.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 7041,
		"Directory": "src/img/stim/i7041.jpg",
		"Type": "iaps",
		"Description": "WoodBaskets",
		"IAPSID": "n7"
	},
	"n8": {
		"Image": "i7053.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 7053,
		"Directory": "src/img/stim/i7053.jpg",
		"Type": "iaps",
		"Description": "CandleStick",
		"IAPSID": "n8"
	},
	"n9": {
		"Image": "i7493.jpg",
		"Emotion": "neutral",
		"Duration": 4500,
		"imgNum": 7493,
		"Directory": "src/img/stim/i7493.jpg",
		"Type": "iaps",
		"Description": "ManonCornr",
		"IAPSID": "n9"
	},
	"s0": {
		"Image": "i2141.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 2141,
		"Directory": "src/img/stim/i2141.jpg",
		"Type": "iaps",
		"Description": "CryingOld",
		"IAPSID": "s0"
	},
	"s1": {
		"Image": "i2205.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 2205,
		"Directory": "src/img/stim/i2205.jpg",
		"Type": "iaps",
		"Description": "SadOldMan",
		"IAPSID": "s1"
	},
	"s2": {
		"Image": "i2276.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 2276,
		"Directory": "src/img/stim/i2276.jpg",
		"Type": "iaps",
		"Description": "CryingGirl",
		"IAPSID": "s2"
	},
	"s3": {
		"Image": "i2455.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 2455,
		"Directory": "src/img/stim/i2455.jpg",
		"Type": "iaps",
		"Description": "SadGirls",
		"IAPSID": "s3"
	},
	"s4": {
		"Image": "i2700.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 2700,
		"Directory": "src/img/stim/i2700.jpg",
		"Type": "iaps",
		"Description": "SadLadies",
		"IAPSID": "s4"
	},
	"s5": {
		"Image": "i2703.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 2703,
		"Directory": "src/img/stim/i2703.jpg",
		"Type": "iaps",
		"Description": "SadKids",
		"IAPSID": "s5"
	},
	"s6": {
		"Image": "i2799.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 2799,
		"Directory": "src/img/stim/i2799.jpg",
		"Type": "iaps",
		"Description": "Funeral",
		"IAPSID": "s6"
	},
	"s7": {
		"Image": "i2900.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 2900,
		"Directory": "src/img/stim/i2900.jpg",
		"Type": "iaps",
		"Description": "CryingBoy",
		"IAPSID": "s7"
	},
	"s8": {
		"Image": "i9421.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 9421,
		"Directory": "src/img/stim/i9421.jpg",
		"Type": "iaps",
		"Description": "CryingSoldier",
		"IAPSID": "s8"
	},
	"s9": {
		"Image": "i9530.jpg",
		"Emotion": "sad",
		"Duration": 4500,
		"imgNum": 9530,
		"Directory": "src/img/stim/i9530.jpg",
		"Type": "iaps",
		"Description": "DirtyKids",
		"IAPSID": "s9"
	}
}