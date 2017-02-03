
      function startIntro(){
        var intro = introJs();
          intro.setOptions({
            steps: [
              {
                element: '#stratify',
                intro: "iSAT, is a tool to generate Stratified Attribute Tracking (SAT) diagram and visualise cohort transitions across attributes. Users can interactively get the transition values and patterns.",
                position: 'top'
              },
              {
                element: '#uploader',
                intro: 'Upload a csv file with each record having: </br><span style="color: blue;">primary key value</span>, attribute value 1, attributte value 2, attribute value 3 <br/>'
              },
              {
                element: '#stratify',
                intro: 'Stratification criteria can be adjusted (work in progress)',
                position: 'left'
              },
              {
                element: '#pattern-panel',
                intro: 'This panel can assist you to highlight some of the basic patterns which emerge in your data-set'
              },
              {
                element: '#restore1',
                intro: 'Use to refresh the SAT Diagram',
                position: 'top'
              },

              {
                element: '#align3',
                intro: 'This highlights the cohort (number of records) that remain in the same stratum across phases',
              },
              {
                element: '#starBurst',
                intro: 'Highlights cohort transitions to a <span style="color:green;">more desirable stratum</span>',
                position: 'bottom'
              },
              {
                element: '#slide',
                intro: 'Highlights cohort transitions to a <span style="color:red;">less desirable stratum </span>'
              },
              {
                element: '#align2',
                intro: 'This highlights the cohort that remain in the same stratum <strong> only between two phases </strong>'
              },
              {
                element: '#switch',
                intro: 'Highlights the strata and the transitions where there are switching between two phases'
              },
              {
                element: '#returnP',
                intro: 'Highlights the cohort which has same attribute value in the first and third phases'
              },
              {
                element: '#voidS',
                intro: 'Highlights the links where transitions dont happen '
              },
              {
                element: '#attr',
                intro: 'Search for the cohort which gets attracted to a specific stratum'
              },
              {
                element: '#ePattern',
                intro: 'Search for any specific cohort transition across three phases'
              }
            ]
          });

          intro.start();
      }
