ed, almost directly, on https://github.com/khuyentran1401/rich-dataframe 
# Building it in because it is small and hasn't been updated much in a while &
# most importantly because I want to customize how it handles the captioning.
# I put this in my fork of https://github.com/khuyentran1401/rich-dataframe now .
# SPECIFIC CUSTOMIZATIONS:
#-------------------------
# I don't want the caption describing how many rows or cols shown unless number 
# of rows or columns is larger than how many are shown.
# Plus, adding note to install rich.
# Plus, removing the animation to the 'beat' because it causes weird spacing
# in Jupyter and I had already turned the speed up so high because I wasn't
# interested in the animated aspect that the default rich-dataframe makes.
# To do this and get output to show up even when using `%run` in Jupyter,
# I had to define the color and style of the columns when first made instead
# of updating after using the beat, `_add_random_color()`, & `_add_style()`,
# AND DELETE `with Live()`.
# Plus, removed `_change_width()` section since I'm not seeing a difference
# without it when not running animation.
#-------------------------
# Adding this in this section of my script so only need rich installed if
# using command line. Use of the main function directly wouldn't necessarily
# need the code handling printng the dataframe in the terminal and so best
# rich not required in such cases so not asking user to install something
# that isn't used.
try:
   from rich import print
except ImportError:
   sys.stderr.write("Run `pip install rich` on your command line "
       "or if\nusing in a Jupyter notebook, run `%pip install rich`"
       ", without the tick marks.\n**EXITING.**.\n")
   sys.exit(1)
from rich.box import MINIMAL, SIMPLE, SIMPLE_HEAD, SQUARE
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.measure import Measurement
from rich.table import Table
console = Console()
COLORS = ["cyan", "magenta", "red", "green", "blue", "purple"]
class DataFramePrettify:
   """Create animated and pretty Pandas DataFrame

   Parameters
   ----------
   df : pd.DataFrame
       The data you want to prettify
   row_limit : int, optional
       Number of rows to show, by default 20
   col_limit : int, optional
       Number of columns to show, by default 10
   first_rows : bool, optional
       Whether to show first n rows or last n rows, by default True. If this is set to False, show last n rows.
   first_cols : bool, optional
       Whether to show first n columns or last n columns, by default True. If this is set to False, show last n rows.
   delay_time : int, optional
       How fast is the animation, by default 5. Increase this to have slower animation.
   clear_console: bool, optional
        Clear the console before printing the table, by default True. If this is set to False the previous console input/output is maintained
   """
   def __init__(
       self,
       df: pd.DataFrame,
       row_limit: int = 20,
       col_limit: int = 10,
       first_rows: bool = True,
       first_cols: bool = True,
       delay_time: int = 5,
       clear_console: bool = True,
   ) -> None:
       self.df = df.reset_index().rename(columns={"index": ""})
       self.table = Table(show_footer=False)
       self.table_centered = Columns(
           (self.table,), align="center", expand=True
       )
       self.num_colors = len(COLORS)
       self.delay_time = delay_time
       self.row_limit = row_limit
       self.first_rows = first_rows
       self.col_limit = col_limit
       self.first_cols = first_cols
       self.clear_console = clear_console
       if first_cols:
           self.columns = self.df.columns[:col_limit]
       else:
           self.columns = list(self.df.columns[-col_limit:])
           self.columns.insert(0, "index")

       if first_rows:
           self.rows = self.df.values[:row_limit]
       else:
           self.rows = self.df.values[-row_limit:]

       if self.clear_console:
           console.clear()

   def _add_columns(self):
       for i,col in enumerate(self.columns):
           color4col = COLORS[i % self.num_colors]# based on https://github.com/khuyentran1401/rich-dataframe/blob/fff92c5fb735babcec580b88ef94b9325b5b8558/rich_dataframe/rich_dataframe.py#L110
           self.table.add_column(str(col),style="bold "+color4col, header_style="bold "+color4col,) # based on https://rich.readthedocs.io/en/stable/tables.html#tables 
           # and https://github.com/khuyentran1401/rich-dataframe/blob/fff92c5fb735babcec580b88ef94b9325b5b8558/rich_dataframe/rich_dataframe.py#L110
   def _add_rows(self):
       for row in self.rows:
           if self.first_cols:
               row = row[: self.col_limit]
           else:
               row = row[-self.col_limit :]
           row = [str(item) for item in row]
           self.table.add_row(*list(row))
   def _move_text_to_right(self):
       for i in range(len(self.table.columns)):
           self.table.columns[i].justify = "right"
   def _adjust_box(self):
       for box in [SIMPLE_HEAD, SIMPLE, MINIMAL, SQUARE]:
           self.table.box = box
   def _dim_row(self):
       self.table.row_styles = ["none", "dim"]
   def _adjust_border_color(self):
       self.table.border_style = "bright_yellow"
   def _add_caption(self):
       if self.first_rows:
           row_text = "first"
       else:
           row_text = "last"
       if self.first_cols:
           col_text = "first"
       else:
           col_text = "last"

       if (len(self.df) > self.row_limit) and (len(self.df.columns) > self.col_limit):
           self.table.caption = f"Only the [bold magenta not dim] {row_text} {self.row_limit} rows[/bold magenta not dim] and the [bold green not dim]{col_text} {self.col_limit} columns[/bold green not dim] are shown here."
       elif len(self.df) > self.row_limit:
           self.table.caption = f"Only the [bold magenta not dim] {row_text} {self.row_limit} rows[/bold magenta not dim] are shown here."
       elif len(self.df.columns) > self.col_limit:
           self.table.caption = f"Only  the [bold green not dim]{col_text} {self.col_limit} columns[/bold green not dim] are shown here."

   def prettify(self):
       self._add_columns()
       self._add_rows()
       self._move_text_to_right()
       self._adjust_border_color()
       self._add_caption()
       console.print(self.table) # based on https://rich.readthedocs.io/en/stable/tables.html#tables and https://stackoverflow.com/a/72747970/8508004
       return self.table
def prettify(
   df: pd.DataFrame,
   row_limit: int = 20,
   col_limit: int = 10,
   first_rows: bool = True,
   first_cols: bool = True,
   delay_time: int = 5,
   clear_console: bool = True,
):
   """Create animated and pretty Pandas DataFrame

   Parameters
   ----------
   df : pd.DataFrame
       The data you want to prettify
   row_limit : int, optional
       Number of rows to show, by default 20
   col_limit : int, optional
       Number of columns to show, by default 10
   first_rows : bool, optional
       Whether to show first n rows or last n rows, by default True. If this is set to False, show last n rows.
   first_cols : bool, optional
       Whether to show first n columns or last n columns, by default True. If this is set to False, show last n rows.
   delay_time : int, optional
       How fast is the animation, by default 5. Increase this to have slower animation.
   clear_console: bool, optional
       Clear the console before priting the table, by default True. If this is set to false the previous console input/output is maintained
   """
   if isinstance(df, pd.DataFrame) or isinstance(df, pd.DataFrame):
       DataFramePrettify(
           df, row_limit, col_limit, first_rows, first_cols, delay_time,clear_console
       ).prettify()

   else:
       # In case users accidentally pass a non-datafame input, use rich's print instead
       print(df)
###---------------END OF CUSTOMIZED RICH-DATAFRAME--------------------------###
