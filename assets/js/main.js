/* GLM Omnimedia News — client-side helpers (no build step, no dependencies) */
(function () {
  "use strict";

  // Current date in the utility bar (client's locale)
  var dateEl = document.getElementById("today-date");
  if (dateEl) {
    try {
      dateEl.textContent = new Date().toLocaleDateString("en-US", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
      });
    } catch (e) {
      dateEl.textContent = "";
    }
  }

  // Verse of the day — rotates by day of year
  var verses = [
    { text: "Thy word is a lamp unto my feet, and a light unto my path.", ref: "Psalm 119:105 (KJV)" },
    { text: "Heaven and earth shall pass away, but my words shall not pass away.", ref: "Matthew 24:35 (KJV)" },
    { text: "All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness.", ref: "2 Timothy 3:16 (KJV)" },
    { text: "The grass withereth, the flower fadeth: but the word of our God shall stand for ever.", ref: "Isaiah 40:8 (KJV)" },
    { text: "Let your light so shine before men, that they may see your good works, and glorify your Father which is in heaven.", ref: "Matthew 5:16 (KJV)" },
    { text: "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.", ref: "John 3:16 (KJV)" },
    { text: "Be not conformed to this world: but be ye transformed by the renewing of your mind.", ref: "Romans 12:2 (KJV)" },
    { text: "Preach the word; be instant in season, out of season; reprove, rebuke, exhort with all longsuffering and doctrine.", ref: "2 Timothy 4:2 (KJV)" },
    { text: "The night is far spent, the day is at hand: let us therefore cast off the works of darkness, and let us put on the armour of light.", ref: "Romans 13:12 (KJV)" },
    { text: "And ye shall know the truth, and the truth shall make you free.", ref: "John 8:32 (KJV)" },
    { text: "Go ye into all the world, and preach the gospel to every creature.", ref: "Mark 16:15 (KJV)" },
    { text: "Blessed are they that hear the word of God, and keep it.", ref: "Luke 11:28 (KJV)" },
    { text: "For the word of God is quick, and powerful, and sharper than any twoedged sword.", ref: "Hebrews 4:12 (KJV)" },
    { text: "A city that is set on an hill cannot be hid.", ref: "Matthew 5:14 (KJV)" }
  ];

  var verseText = document.getElementById("verse-text");
  var verseRef = document.getElementById("verse-ref");
  if (verseText && verseRef) {
    var now = new Date();
    var start = new Date(now.getFullYear(), 0, 0);
    var dayOfYear = Math.floor((now - start) / 86400000);
    var v = verses[dayOfYear % verses.length];
    verseText.textContent = "\u201C" + v.text + "\u201D";
    verseRef.textContent = v.ref;
  }
})();
