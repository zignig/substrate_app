{
   "author": {
       "map": "function (doc) {\n\t\t\tif(doc.author){\n\t\t\t\temit(doc.author,{name:doc.name,author:doc.author,thumb:doc.thumb});\n\t\t\t}\n        }"
   },
   "author_list": {
       "map": "function (doc) {\n\t\t\tif(doc.author){\n\t\t\t\temit([doc.author[0].toLowerCase(),doc.author],1);\n\t\t\t}\n\t}",
       "reduce": "_count"
   },
   "tag": {
       "map": "function (doc) {\n\t\t\tif (!doc.tags){return;}\n\t    for (var i = 0; i < doc.tags.length; ++i) {\n\t\t\t\temit(doc.tags[i],{name:doc.name,author:doc.author,thumb:doc.thumb});\n\t\t\t}\n        }"
   },
   "author_alpha": {
       "map": "function (doc) {\n\t\t\tif(doc.author){\n\t\t\t\temit(doc.author[0].toLowerCase(),doc.author);\n\t\t\t}\n\t}",
       "reduce": "_count"
   },
   "home": {
       "map": "function (doc) {\n\t\t\tif(doc.thumb){\n\t\t\t\temit(doc.updated_at,{name:doc.name,author:doc.author,thumb:doc.thumb});\n\t\t\t}\n        }"
   },
   "tag_alpha": {
       "map": "function (doc) {\n            if(doc.tags){\n\t    \t\tfor (var i = 0; i < doc.tags.length; ++i) {\n                \temit(doc.tags[i][0].toLowerCase(),doc.tags[i]);\n\t\t\t\t}\n            }\n    }",
       "reduce": "_count"
   },
   "seen": {
       "map": "function (doc) { \n\t\t\tif (doc.seen === void 0) {\n\t\t\t\temit(doc.name,{name:doc.name,author:doc.author,thumb:doc.thumb});\n\t\t\t}\n\t}"
   },
   "tag_list": {
       "map": "function (doc) {\n            if(doc.tags){\n\t    \t\tfor (var i = 0; i < doc.tags.length; ++i) {\n                \temit([doc.tags[i][0].toLowerCase(),doc.tags[i]],1);\n\t\t\t\t}\n            }\n    }",
       "reduce": "_count"
   }
}
