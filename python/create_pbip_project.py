import os
import json

def create_pbip():
    base_dir = 'powerbi'
    report_dir = os.path.join(base_dir, 'Customer_Voice_Analytics.Report')
    dataset_dir = os.path.join(base_dir, 'Customer_Voice_Analytics.Dataset')
    
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(dataset_dir, exist_ok=True)
    
    # 1. Customer_Voice_Analytics.pbip (Root Pointer File)
    pbip_content = {
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": "Customer_Voice_Analytics.Report"
                }
            }
        ]
    }
    with open(os.path.join(base_dir, 'Customer_Voice_Analytics.pbip'), 'w', encoding='utf-8') as f:
        json.dump(pbip_content, f, indent=2)
        
    # 2. definition.pbir (Report Link File)
    pbir_content = {
        "version": "1.0",
        "datasetReference": {
            "byPath": {
                "path": "../Customer_Voice_Analytics.Dataset"
            }
        }
    }
    with open(os.path.join(report_dir, 'definition.pbir'), 'w', encoding='utf-8') as f:
        json.dump(pbir_content, f, indent=2)
        
    # 3. definition.pbism (Dataset Link File)
    pbism_content = {
        "version": "1.0"
    }
    with open(os.path.join(dataset_dir, 'definition.pbism'), 'w', encoding='utf-8') as f:
        json.dump(pbism_content, f, indent=2)

    # 4. model.bim (Complete Data Model, M Code Power Query, DAX Measures, Relationships)
    model_bim = {
        "name": "Customer_Voice_Analytics",
        "compatibilityLevel": 1567,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "tables": [
                {
                    "name": "feedback",
                    "columns": [
                        {"name": "response_id", "dataType": "string", "sourceColumn": "response_id"},
                        {"name": "customer_id", "dataType": "string", "sourceColumn": "customer_id"},
                        {"name": "survey_date", "dataType": "dateTime", "sourceColumn": "survey_date", "formatString": "yyyy-MM-dd"},
                        {"name": "region", "dataType": "string", "sourceColumn": "region"},
                        {"name": "customer_segment", "dataType": "string", "sourceColumn": "customer_segment"},
                        {"name": "industry", "dataType": "string", "sourceColumn": "industry"},
                        {"name": "response_channel", "dataType": "string", "sourceColumn": "response_channel"},
                        {"name": "service_category", "dataType": "string", "sourceColumn": "service_category"},
                        {"name": "nps_score", "dataType": "int64", "sourceColumn": "nps_score"},
                        {"name": "csat_score", "dataType": "int64", "sourceColumn": "csat_score"},
                        {"name": "resolution_days", "dataType": "int64", "sourceColumn": "resolution_days"},
                        {"name": "issue_resolved", "dataType": "string", "sourceColumn": "issue_resolved"},
                        {"name": "feedback_text", "dataType": "string", "sourceColumn": "feedback_text"},
                        {
                            "name": "nps_category",
                            "dataType": "string",
                            "type": "calculated",
                            "expression": "IF(feedback[nps_score] >= 9, \"Promoter\", IF(feedback[nps_score] >= 7, \"Passive\", \"Detractor\"))"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "feedback-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = Json.Document(Web.Contents(\"http://127.0.0.1:8000/api/feedback\")),",
                                    "    #\"Converted to Table\" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),",
                                    "    #\"Expanded Column1\" = Table.ExpandRecordColumn(#\"Converted to Table\", \"Column1\", {\"response_id\", \"customer_id\", \"survey_date\", \"region\", \"customer_segment\", \"industry\", \"response_channel\", \"service_category\", \"nps_score\", \"csat_score\", \"resolution_days\", \"issue_resolved\", \"feedback_text\"}),",
                                    "    #\"Changed Type\" = Table.TransformColumnTypes(#\"Expanded Column1\",{{\"response_id\", type text}, {\"customer_id\", type text}, {\"survey_date\", type date}, {\"region\", type text}, {\"customer_segment\", type text}, {\"industry\", type text}, {\"response_channel\", type text}, {\"service_category\", type text}, {\"nps_score\", Int64.Type}, {\"csat_score\", Int64.Type}, {\"resolution_days\", Int64.Type}, {\"issue_resolved\", type text}, {\"feedback_text\", type text}})",
                                    "in",
                                    "    #\"Changed Type\""
                                ]
                            }
                        }
                    ],
                    "measures": [
                        {
                            "name": "Total Responses",
                            "expression": "COUNTROWS(feedback)",
                            "formatString": "#,0"
                        },
                        {
                            "name": "Promoters",
                            "expression": "CALCULATE(COUNTROWS(feedback), feedback[nps_score] >= 9)",
                            "formatString": "#,0"
                        },
                        {
                            "name": "Passives",
                            "expression": "CALCULATE(COUNTROWS(feedback), feedback[nps_score] = 7 || feedback[nps_score] = 8)",
                            "formatString": "#,0"
                        },
                        {
                            "name": "Detractors",
                            "expression": "CALCULATE(COUNTROWS(feedback), feedback[nps_score] <= 6)",
                            "formatString": "#,0"
                        },
                        {
                            "name": "Promoter %",
                            "expression": "DIVIDE([Promoters], [Total Responses], 0)",
                            "formatString": "0.00%"
                        },
                        {
                            "name": "Detractor %",
                            "expression": "DIVIDE([Detractors], [Total Responses], 0)",
                            "formatString": "0.00%"
                        },
                        {
                            "name": "NPS",
                            "expression": "([Promoter %] - [Detractor %]) * 100",
                            "formatString": "+0.0;-0.0;0.0"
                        },
                        {
                            "name": "Average CSAT",
                            "expression": "AVERAGE(feedback[csat_score])",
                            "formatString": "0.00"
                        },
                        {
                            "name": "Average Resolution Days",
                            "expression": "AVERAGE(feedback[resolution_days])",
                            "formatString": "0.00"
                        }
                    ]
                },
                {
                    "name": "Dim_Date",
                    "dataCategory": "Time",
                    "columns": [
                        {"name": "Date", "dataType": "dateTime", "isKey": True, "sourceColumn": "Date", "formatString": "yyyy-MM-dd"},
                        {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
                        {"name": "Quarter", "dataType": "string", "sourceColumn": "Quarter"},
                        {"name": "MonthNo", "dataType": "int64", "sourceColumn": "MonthNo"},
                        {"name": "MonthName", "dataType": "string", "sourceColumn": "MonthName"},
                        {"name": "YearMonth", "dataType": "string", "sourceColumn": "YearMonth"}
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Date-Partition",
                            "mode": "import",
                            "source": {
                                "type": "calculated",
                                "expression": [
                                    "VAR MinDate = MIN(feedback[survey_date])",
                                    "VAR MaxDate = MAX(feedback[survey_date])",
                                    "RETURN",
                                    "ADDCOLUMNS(",
                                    "    CALENDAR(MinDate, MaxDate),",
                                    "    \"Year\", YEAR([Date]),",
                                    "    \"Quarter\", \"Q\" & FORMAT([Date], \"Q\"),",
                                    "    \"MonthNo\", MONTH([Date]),",
                                    "    \"MonthName\", FORMAT([Date], \"MMM\"),",
                                    "    \"YearMonth\", FORMAT([Date], \"YYYY-MM\")",
                                    ")"
                                ]
                            }
                        }
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "Rel_Date_Feedback",
                    "fromTable": "feedback",
                    "fromColumn": "survey_date",
                    "toTable": "Dim_Date",
                    "toColumn": "Date",
                    "crossFilteringBehavior": "oneDirection"
                }
            ]
        }
    }
    with open(os.path.join(dataset_dir, 'model.bim'), 'w', encoding='utf-8') as f:
        json.dump(model_bim, f, indent=2)

    # 5. report.json (Page Layout & Visual Configuration)
    report_json = {
        "config": json.dumps({
            "version": "5.50",
            "themeCollection": {"baseTheme": {"name": "CY24SU06", "version": "5.50", "type": 2}},
            "activeSectionName": "CustomerExperienceOverview"
        }),
        "sections": [
            {
                "name": "CustomerExperienceOverview",
                "displayName": "Customer Experience Overview",
                "filters": "[]",
                "height": 720,
                "width": 1280,
                "visualContainers": [
                    {
                        "x": 20, "y": 20, "z": 0, "width": 1240, "height": 60,
                        "config": json.dumps({"name": "HeaderBanner", "title": "Customer Voice & NPS Analytics"})
                    },
                    {
                        "x": 20, "y": 90, "z": 1, "width": 290, "height": 100,
                        "config": json.dumps({"name": "Card_TotalResponses", "title": "Total Responses", "measure": "[Total Responses]"})
                    },
                    {
                        "x": 330, "y": 90, "z": 2, "width": 290, "height": 100,
                        "config": json.dumps({"name": "Card_NPS", "title": "Net NPS", "measure": "[NPS]"})
                    },
                    {
                        "x": 640, "y": 90, "z": 3, "width": 290, "height": 100,
                        "config": json.dumps({"name": "Card_CSAT", "title": "Average CSAT", "measure": "[Average CSAT]"})
                    },
                    {
                        "x": 950, "y": 90, "z": 4, "width": 290, "height": 100,
                        "config": json.dumps({"name": "Card_PromoterShare", "title": "Promoter Share", "measure": "[Promoter %]"})
                    },
                    {
                        "x": 20, "y": 200, "z": 5, "width": 600, "height": 240,
                        "config": json.dumps({"name": "Line_MonthlyNPSTrend", "title": "Monthly NPS Trend"})
                    },
                    {
                        "x": 640, "y": 200, "z": 6, "width": 600, "height": 240,
                        "config": json.dumps({"name": "Bar_NPSByRegion", "title": "NPS by Region"})
                    },
                    {
                        "x": 20, "y": 450, "z": 7, "width": 390, "height": 240,
                        "config": json.dumps({"name": "Donut_NPSCategoryDistribution", "title": "NPS Category Distribution (Promoters vs Passives vs Detractors)"})
                    },
                    {
                        "x": 430, "y": 450, "z": 8, "width": 500, "height": 240,
                        "config": json.dumps({"name": "Bar_CSATBySegment", "title": "Average CSAT by Customer Segment"})
                    },
                    {
                        "x": 950, "y": 450, "z": 9, "width": 290, "height": 240,
                        "config": json.dumps({"name": "Bar_ChannelVolume", "title": "Response Volume by Channel"})
                    }
                ]
            },
            {
                "name": "VoiceOfCustomerAnalysis",
                "displayName": "Voice of Customer Analysis",
                "filters": "[]",
                "height": 720,
                "width": 1280,
                "visualContainers": [
                    {
                        "x": 20, "y": 20, "z": 0, "width": 1240, "height": 60,
                        "config": json.dumps({"name": "HeaderBanner2", "title": "Voice of Customer Analysis"})
                    },
                    {
                        "x": 20, "y": 90, "z": 1, "width": 600, "height": 200,
                        "config": json.dumps({"name": "Bar_ServiceCategoryVolume", "title": "Response Distribution by Service Category"})
                    },
                    {
                        "x": 640, "y": 90, "z": 2, "width": 600, "height": 200,
                        "config": json.dumps({"name": "Bar_NPSByServiceCategory", "title": "NPS by Service Category"})
                    },
                    {
                        "x": 20, "y": 300, "z": 3, "width": 600, "height": 200,
                        "config": json.dumps({"name": "Bar_NPSBySegment2", "title": "NPS by Customer Segment"})
                    },
                    {
                        "x": 640, "y": 300, "z": 4, "width": 600, "height": 200,
                        "config": json.dumps({"name": "Bar_ResolutionDaysByNPS", "title": "Average Resolution Days by NPS Category"})
                    },
                    {
                        "x": 20, "y": 510, "z": 5, "width": 1220, "height": 190,
                        "config": json.dumps({"name": "Table_LowNPSFeedback", "title": "Low-NPS Customer Feedback Detail Table (NPS <= 6)"})
                    }
                ]
            }
        ]
    }
    with open(os.path.join(report_dir, 'report.json'), 'w', encoding='utf-8') as f:
        json.dump(report_json, f, indent=2)

    print("Power BI Project (.pbip) artifact generation completed successfully!")

if __name__ == '__main__':
    create_pbip()
