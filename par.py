# pan.py -- PSEB Analyse Results
#
#   A script to analyse the 10th and 12th school results downloaded as an xlsx file from the PSEB site.
#   The results are saved to 'processed' and 'performance' sheets of the same xlsx file.
#

import pandas as pd
import re
import argparse
import sys

# use code from pnb2unicode.py
# from pnb2unicode import to_unicode 
import pnb2unicode

def extract_subjects_with_grades(text):
    if pd.isna(text):
        return {}

    parts = [part.strip() for part in str(text).split('|') if part.strip()]
    subject_data = {}

    for part in parts:
        match = re.match(r'(?P<subject>[A-Z]{2,5})- (?P<marks>[\d+ =]+)\s+\((?P<grade>[A-Z+]+)\)', part)
        if match:
            sub = match.group('subject')
            marks = match.group('marks').strip()
            grade = match.group('grade').strip()
            subject_data[f"{sub}_marks"] = marks
            subject_data[f"{sub}_grade"] = grade
        else:
            fallback = re.match(r'(?P<subject>[A-Z]{2,5})- (?P<marks>.+)', part)
            if fallback:
                sub = fallback.group('subject')
                marks = fallback.group('marks').strip()
                subject_data[f"{sub}_marks"] = marks
                subject_data[f"{sub}_grade"] = ""
    return subject_data

def process_excel(file_path):
    df = pd.read_excel(file_path, sheet_name='Table')   # the sheet name 'Table' comes from the downloaded data
#    if 'nm' in df.columns:
#        nm_index = df.columns.get_loc('nm')
#        # Insert a blank 'Section' column after 'nm'
#        df.insert(nm_index + 1, 'Section', "")

    # Step 1: Parse 'detailres' column
    if 'detailres' in df.columns:
        extracted_df = df['detailres'].apply(extract_subjects_with_grades)
        subjects_df = pd.DataFrame(extracted_df.tolist()).fillna("")
#        print(subjects_df)
#        exit(1)
        df = pd.concat([df.drop(columns=['detailres']), subjects_df], axis=1)

    # Step 2: Extract totals from *_marks
    for col in df.columns:
        if col.endswith('_marks') and df[col].dtype == object:
            marks_before_eq = []
            marks_total = []

            for val in df[col]:
                if isinstance(val, str) and '=' in val:
                    parts = val.split('=', 1)
                    marks_before_eq.append(parts[0].strip())
                    try:
                        marks_total.append(int(parts[1].strip()))
                    except ValueError:
                        marks_total.append(None)
                else:
                    marks_before_eq.append(val)
                    marks_total.append(None)

            df[col] = marks_before_eq
            temp_total_col = col.replace('_marks', '_marks_total')
            df[temp_total_col] = marks_total

    # Step 3: Replace *_grade with *_marks_total → rename to *_total
    for col in list(df.columns):
        if col.endswith('_grade'):
            subject_prefix = col.replace('_grade', '')
            temp_total_col = f"{subject_prefix}_marks_total"
            final_total_col = f"{subject_prefix}_total"

            if temp_total_col in df.columns:
                df[final_total_col] = df[temp_total_col]

            df.drop(columns=[col], inplace=True)
            if temp_total_col in df.columns:
                df.drop(columns=[temp_total_col], inplace=True)

    # Step 4: Drop unwanted columns if present
    for drop_col in ['schlNMP', 'SCHLNCODE', 'SCHLSET']:
        if drop_col in df.columns:
            df.drop(columns=[drop_col], inplace=True)

     # Step 5: Rearrange *_total columns to appear right after their *_marks columns
    new_column_order = []
    used_cols = set()

    for col in df.columns:
        if col.endswith('_marks') and col not in used_cols:
            new_column_order.append(col)
            used_cols.add(col)
            total_col = col.replace('_marks', '_total')
            if total_col in df.columns:
                new_column_order.append(total_col)
                used_cols.add(total_col)

    # Add all other columns (non-_marks/_total) at the beginning
    remaining_cols = [col for col in df.columns if col not in used_cols]
    df = df[remaining_cols + new_column_order]

    # convert name 'nm' column to unicode
    df['nm'] = df['nm'].apply(pnb2unicode.to_unicode)


    ## ~Step 6: Save output~
    #    output_file = file_path.replace('.xlsx', '_processed.xlsx')
    #    df.to_excel(output_file, index=False)

    # Step 6: Save output to 'processed' sheet of the same file
    #    df.to_excel(file_path, sheet_name='processed', if_sheet_exists='replace', index=False)
    with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='processed')

    print(f"Processed result saved to 'processed' sheet of {file_path}")


    ######## now do the performance analysis ##############

    student_sheet = 'processed'
    max_sheet = 'MM'
    excel_file = file_path
    default_max = 100
    
    # --- Load data ---
    try:
        students_df = pd.read_excel(excel_file, sheet_name=student_sheet)
        max_df = pd.read_excel(excel_file, sheet_name=max_sheet)
    except ValueError as e:
        print(f"❌ Sheet loading error: {e}")
        sys.exit(1)


    # --- Clean max marks data ---
    max_df.columns = [col.strip() for col in max_df.columns]
    max_marks_dict = dict(zip(max_df["Subject"], max_df["MM"]))

    # --- Validate 'Section' column ---
    if "Section" not in students_df.columns:
        print("❌ 'Section' column not found in student sheet.")
        sys.exit(1)

    # --- Generate section-wise summary using _total columns ---
    summary = []
    found_subjects = [col for col in students_df.columns if col.endswith("_total")]

    if not found_subjects:
        print("❌ No '_total' columns found in the student sheet.")
        sys.exit(1)

    print("\n--- Section-wise Summary (Based on '_total' columns) ---")
    for section, section_df in students_df.groupby("Section"):
        print(f"\n🔹 Processing Section: {section}")
        serial_no = 1
        for col in found_subjects:
            subject = col.replace("_total", "")
            max_marks = pd.to_numeric(max_marks_dict.get(subject, default_max), errors="coerce")

            if pd.isna(max_marks) or max_marks == 0:
                print(f"⚠️  Skipping '{subject}': No max marks found or invalid")
                continue

            marks_series = pd.to_numeric(section_df[col], errors="coerce")
            valid_count = marks_series.notnull().sum()
            print(f"✅ {subject}: Found {valid_count} valid scores in Section {section} (Max = {max_marks})")

            if valid_count == 0:
                print(f"⚠️  Skipping '{subject}' in Section {section}: No valid numeric marks")
                continue

            percent_series = (marks_series / max_marks) * 100
            count_60 = (percent_series > 60).sum()
            count_75 = (percent_series > 75).sum()

            summary.append({
                "S.No.": serial_no,
                "Section": section,
                "Subject": subject,
                "Max Marks": max_marks,
                "Valid Scores": valid_count,
                "Students > 60%": count_60,
                "Students > 75%": count_75
            })
            serial_no += 1

    # --- Output summary to ~CSV~ 'performace' sheet ---
    if not summary:
        print("❌ No valid data found to generate summary.")
    else:
        summary_df = pd.DataFrame(summary)
        # Rearrange columns to place 'S.No.' at the start
        cols = ["S.No."] + [col for col in summary_df.columns if col != "S.No."]
        summary_df = summary_df[cols]

        with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
            summary_df.to_excel(writer, sheet_name='performance')
            print(f"\n✅ Section-wise report saved to 'performance' sheet of '{file_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Excel: extract, split, drop specific columns, and reorder.")
    parser.add_argument("filepath", help="Path to the Excel file")
    args = parser.parse_args()
    process_excel(args.filepath)

