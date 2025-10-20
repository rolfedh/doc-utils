"""
AsciiDoc Table Parser Module

Parses AsciiDoc tables and extracts structured data. Designed to be reusable
for various table conversion tasks (not just callout explanations).

Handles:
- Two-column tables with callout numbers and explanations
- Conditional statements (ifdef, ifndef, endif) within table cells
- Multi-line table cells
- Table attributes and formatting
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TableCell:
    """Represents a single table cell with its content and any conditional blocks."""
    content: List[str]  # Lines of content in the cell
    conditionals: List[str]  # Any ifdef/ifndef/endif lines associated with this cell


@dataclass
class TableRow:
    """Represents a table row with cells."""
    cells: List[TableCell]
    conditionals_before: List[str]  # Conditional statements before this row
    conditionals_after: List[str]  # Conditional statements after this row


@dataclass
class AsciiDocTable:
    """Represents a complete AsciiDoc table."""
    start_line: int
    end_line: int
    attributes: str  # Table attributes like [cols="1,3"]
    rows: List[TableRow]


class TableParser:
    """Parses AsciiDoc tables and extracts structured data."""

    # Pattern for table start delimiter with optional attributes
    TABLE_START = re.compile(r'^\[.*?\]$')
    TABLE_DELIMITER = re.compile(r'^\|===\s*$')

    # Pattern for table cell separator
    CELL_SEPARATOR = re.compile(r'^\|')

    # Pattern for conditional directives
    IFDEF_PATTERN = re.compile(r'^(ifdef::|ifndef::).+\[\]\s*$')
    ENDIF_PATTERN = re.compile(r'^endif::\[\]\s*$')

    # Pattern for callout number (used for callout table detection)
    CALLOUT_NUMBER = re.compile(r'^<(\d+)>\s*$')

    def find_tables(self, lines: List[str]) -> List[AsciiDocTable]:
        """Find all tables in the document."""
        tables = []
        i = 0

        while i < len(lines):
            # Look for table delimiter
            if self.TABLE_DELIMITER.match(lines[i]):
                # Check if there are attributes on the line before
                attributes = ""
                start_line = i

                if i > 0 and self.TABLE_START.match(lines[i - 1]):
                    attributes = lines[i - 1]
                    start_line = i - 1

                # Parse table content
                table = self._parse_table(lines, start_line, i)
                if table:
                    tables.append(table)
                    i = table.end_line + 1
                    continue
            i += 1

        return tables

    def _parse_table(self, lines: List[str], start_line: int, delimiter_line: int) -> Optional[AsciiDocTable]:
        """
        Parse a single table starting at the delimiter.

        AsciiDoc table format:
        |===
        |Cell1
        |Cell2
        (blank line separates rows)
        |Cell3
        |Cell4
        |===
        """
        i = delimiter_line + 1
        rows = []
        current_row_cells = []
        current_cell_lines = []
        conditionals_before_row = []
        conditionals_after_row = []

        while i < len(lines):
            line = lines[i]

            # Check for table end
            if self.TABLE_DELIMITER.match(line):
                # Save any pending cell
                if current_cell_lines:
                    current_row_cells.append(TableCell(
                        content=current_cell_lines.copy(),
                        conditionals=[]
                    ))
                    current_cell_lines = []

                # Save any pending row
                if current_row_cells:
                    rows.append(TableRow(
                        cells=current_row_cells.copy(),
                        conditionals_before=conditionals_before_row.copy(),
                        conditionals_after=conditionals_after_row.copy()
                    ))

                # Get attributes if present
                attributes = ""
                if start_line < delimiter_line:
                    attributes = lines[start_line]

                return AsciiDocTable(
                    start_line=start_line,
                    end_line=i,
                    attributes=attributes,
                    rows=rows
                )

            # Check for conditional directives
            if self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line):
                if not current_row_cells:
                    # Conditional before any cells in this row
                    conditionals_before_row.append(line)
                else:
                    # Conditional after cells started - treat as part of current context
                    if current_cell_lines:
                        # Inside a cell
                        current_cell_lines.append(line)
                    else:
                        # Between cells in the same row
                        conditionals_after_row.append(line)
                i += 1
                continue

            # Blank line separates rows
            if not line.strip():
                # Save pending cell if exists
                if current_cell_lines:
                    current_row_cells.append(TableCell(
                        content=current_cell_lines.copy(),
                        conditionals=[]
                    ))
                    current_cell_lines = []

                # Save row if we have cells
                if current_row_cells:
                    rows.append(TableRow(
                        cells=current_row_cells.copy(),
                        conditionals_before=conditionals_before_row.copy(),
                        conditionals_after=conditionals_after_row.copy()
                    ))
                    current_row_cells = []
                    conditionals_before_row = []
                    conditionals_after_row = []

                i += 1
                continue

            # Check for cell separator (|)
            if self.CELL_SEPARATOR.match(line):
                # Save previous cell if exists
                if current_cell_lines:
                    current_row_cells.append(TableCell(
                        content=current_cell_lines.copy(),
                        conditionals=[]
                    ))
                    current_cell_lines = []

                # Extract cell content from this line (text after |)
                cell_content = line[1:].strip()  # Remove leading |
                if cell_content:
                    current_cell_lines.append(cell_content)
                # If empty, just start a new cell with no content yet

                i += 1
                continue

            # Regular content line (continuation of current cell)
            if current_cell_lines or current_row_cells:
                current_cell_lines.append(line)

            i += 1

        # Return None if we didn't find a proper table end
        return None

    def is_callout_table(self, table: AsciiDocTable) -> bool:
        """
        Determine if a table is a callout explanation table.
        A callout table has two columns: callout number and explanation.
        """
        if not table.rows:
            return False

        # Check if all rows have exactly 2 cells
        if not all(len(row.cells) == 2 for row in table.rows):
            return False

        # Check if first cell of each row is a callout number
        for row in table.rows:
            first_cell = row.cells[0]
            if not first_cell.content:
                return False

            # First line of first cell should be a callout number
            first_line = first_cell.content[0].strip()
            if not self.CALLOUT_NUMBER.match(first_line):
                return False

        return True

    def extract_callout_explanations_from_table(self, table: AsciiDocTable) -> Dict[int, Tuple[List[str], List[str]]]:
        """
        Extract callout explanations from a table.
        Returns dict mapping callout number to tuple of (explanation_lines, conditionals).

        The conditionals list includes any ifdef/ifndef/endif statements that should
        be preserved when converting the table to other formats.
        """
        explanations = {}

        for row in table.rows:
            if len(row.cells) != 2:
                continue

            callout_cell = row.cells[0]
            explanation_cell = row.cells[1]

            # Extract callout number
            first_line = callout_cell.content[0].strip()
            match = self.CALLOUT_NUMBER.match(first_line)
            if not match:
                continue

            callout_num = int(match.group(1))

            # Collect explanation lines
            explanation_lines = []
            for line in explanation_cell.content:
                # Skip conditional directives in explanation (preserve them separately)
                if not (self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line)):
                    explanation_lines.append(line)

            # Collect all conditionals for this row
            all_conditionals = []
            all_conditionals.extend(row.conditionals_before)

            # Extract conditionals from explanation cell
            for line in explanation_cell.content:
                if self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line):
                    all_conditionals.append(line)

            all_conditionals.extend(row.conditionals_after)

            explanations[callout_num] = (explanation_lines, all_conditionals)

        return explanations

    def find_callout_table_after_code_block(self, lines: List[str], code_block_end: int) -> Optional[AsciiDocTable]:
        """
        Find a callout explanation table that appears after a code block.

        Args:
            lines: All lines in the document
            code_block_end: Line number where the code block ends

        Returns:
            AsciiDocTable if a callout table is found, None otherwise
        """
        # Skip blank lines and continuation markers after code block
        i = code_block_end + 1
        while i < len(lines) and (not lines[i].strip() or lines[i].strip() == '+'):
            i += 1

        # Look for a table starting within the next few lines
        # (allowing for possible text between code block and table)
        search_limit = min(i + 10, len(lines))

        for j in range(i, search_limit):
            line = lines[j]

            # If we encounter a list-format callout explanation, stop
            # (list format takes precedence over table format further away)
            if self.CALLOUT_NUMBER.match(line.strip()):
                return None

            # If we encounter another code block start, stop
            if line.strip() in ['----', '....'] or line.strip().startswith('[source'):
                return None

            # Check for table delimiter
            if self.TABLE_DELIMITER.match(line):
                # Found a table, parse it
                start_line = j
                if j > 0 and self.TABLE_START.match(lines[j - 1]):
                    start_line = j - 1

                table = self._parse_table(lines, start_line, j)
                if table and self.is_callout_table(table):
                    return table

                # If we found a table but it's not a callout table, stop searching
                break

        return None

    def convert_table_to_deflist(self, table: AsciiDocTable, preserve_conditionals: bool = True) -> List[str]:
        """
        Convert a two-column table to an AsciiDoc definition list.

        Args:
            table: The table to convert
            preserve_conditionals: Whether to preserve ifdef/ifndef/endif statements

        Returns:
            List of lines representing the definition list
        """
        output = []

        for row in table.rows:
            if len(row.cells) != 2:
                continue

            # Add conditionals before row
            if preserve_conditionals and row.conditionals_before:
                output.extend(row.conditionals_before)

            # First cell is the term
            term_lines = row.cells[0].content
            if term_lines:
                output.append(term_lines[0])

            # Second cell is the definition
            definition_lines = row.cells[1].content
            if definition_lines:
                # Filter out conditionals if needed
                if preserve_conditionals:
                    for line in definition_lines:
                        if self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line):
                            output.append(line)
                        else:
                            output.append(f"  {line}")
                else:
                    for line in definition_lines:
                        if not (self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line)):
                            output.append(f"  {line}")

            # Add conditionals after row
            if preserve_conditionals and row.conditionals_after:
                output.extend(row.conditionals_after)

            # Add blank line between entries
            output.append("")

        # Remove trailing blank line
        if output and not output[-1].strip():
            output.pop()

        return output

    def convert_table_to_bullets(self, table: AsciiDocTable, preserve_conditionals: bool = True) -> List[str]:
        """
        Convert a two-column table to a bulleted list.

        Args:
            table: The table to convert
            preserve_conditionals: Whether to preserve ifdef/ifndef/endif statements

        Returns:
            List of lines representing the bulleted list
        """
        output = []

        for row in table.rows:
            if len(row.cells) != 2:
                continue

            # Add conditionals before row
            if preserve_conditionals and row.conditionals_before:
                output.extend(row.conditionals_before)

            # Get the term (first cell)
            term_lines = row.cells[0].content
            term = term_lines[0] if term_lines else ""

            # Get the definition (second cell)
            definition_lines = row.cells[1].content

            # Filter conditionals from definition if needed
            filtered_def_lines = []
            inline_conditionals = []

            for line in definition_lines:
                if self.IFDEF_PATTERN.match(line) or self.ENDIF_PATTERN.match(line):
                    if preserve_conditionals:
                        inline_conditionals.append(line)
                else:
                    filtered_def_lines.append(line)

            # Create bullet item
            if filtered_def_lines:
                first_line = filtered_def_lines[0]
                output.append(f"* *{term}*: {first_line}")

                # Add continuation lines with proper indentation
                for line in filtered_def_lines[1:]:
                    output.append(f"  {line}")

                # Add inline conditionals if present
                if preserve_conditionals and inline_conditionals:
                    output.extend(inline_conditionals)

            # Add conditionals after row
            if preserve_conditionals and row.conditionals_after:
                output.extend(row.conditionals_after)

        return output
