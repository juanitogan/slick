# SLiCk

**SLiCk** : the Slick Layer Combinator for Inkscape

Like so many awesome extensions that came before Slick (none of which, admittedly, I tried, even though I read about many) Slick helps you produce multiple versions of a drawing from a single master drawing.  So, what makes slick different?  Well... um... it's slick!  Slick promotes **intelligent layer and child-layer use** (instead of just one layer per output drawing and unslick stuff like that).

I use Slick for producing game sprites for a top-down game that shades and highlights the sprite in different ways as it rotates in the sunlight.  Thus, each sprite needs eight different versions for the eight rotations.  Another excellent use for Slick might be cartooning in multiple languages.  Others have asked for such a tool for educational drawings of system processes and who-knows-what.

Slick uses convention over configuration wherever Slick can.  Logical, pretty convention.  In fact, I established the convention initially to visually help my _manual_ workflow, so I know it is beautiful.  I only later decided to automate it with a script.  Here's the convention:

| Convention | Example | Description |
|:-----------|:--------|:------------|
| `(`&nbsp;`)` parenthesis          | (ref&nbsp;art)         | Identifies a layer that will always be hidden. Must be the first and last character. |
| `!` exclamation&nbsp;point        | Background!            | Identifies a layer that will always be shown.  Can appear anywhere in the layer name: `Here!`, `h!r!`, `!! Here`, `--here!--`, etc.  But, is meaningless inside parenthesis like `(Here!)`. |
| `--`&nbsp;`--` double&nbsp;dashes | --Fred's&nbsp;dialog-- | Identifies a layer as a _parent layer_ to _option layers_.  That is, each child layer to this layer is what we are calling an "option layer" and option layers are where each variation of the master art will be drawn.  Think of this as a layer containing a list of versions of the art. |
| `,` comma                         | Red,&nbsp;Blue         | When appearing in the name of an option layer, identifies an option layer that will show for more than one option.  The list can be as long as what will fit in a layer name. |
|   | Hello | Any layer not named as above--and not an option layer under a parent layer--will keep it's visibility as is. |

Pretty simple... er... slick, eh?

**NOTE: Use only valid filename characters when naming your option layers.  Do not use slashes (/\\) and other characters that would not be valid in a filename.**

Character case does not matter (even though you might notice that I, personally, use case conventions in the examples).

Now, let's get to the interesting bit: option layers.  Every child layer under a double-dashed parent layer becomes the name of a version of the drawing.  For example, if the `--dialog--` layer contains three layers called `English`, `French`, and `German`, then there is assumed to be three versions of the drawing.  If these were in a drawing called `Cartoon.svg`, Slick will output three files when run:

Cartoon.svg layers:
- (guides)
- --dialog--
  - English
  - French
  - German
- Background

Slick output:
- Cartoon_English.svg
- Cartoon_French.svg
- Cartoon_German.svg

Note that Slick does not delete layers in the output files.  Slick only shows or hides them for you.  I'm not yet sure if I'll add a delete option someday (to help manage file size for those who may need such management... but who?).  For now, I'm going for keeping it simple, and for maximum flexibility with other steps in your art pipeline.

Now, lets take it up a notch with the option layers.  Let's say you have the three languages listed above, but need only two different speech bubbles to fit the different languages in.  To handle that, for example, you might then have a parent layer called `--speech bubbles--` that contains two option layers called `English, French` and `German`.  Run this through Slick and Slick will output the same three files even though there are only two variants to the speech bubble.  You see, Slick looks for commas in option layer names and treats everything separated by a comma as it's own option layer.  Pretty cool... er... slick, eh?

Cartoon.svg layers:
- (guides)
- --speech bubbles--
  - English, French
  - German
- Background

Slick output:
- Cartoon_English.svg
- Cartoon_French.svg
- Cartoon_German.svg

Furthermore, don't worry about spaces (or lack of spaces) around commas in option layer names.  Slick doesn't care about such spaces in option layer names.  Slick doesn't understand why programmers in the early days of the internet found it so hard to help customers out by scrubbing spaces automatically from credit card numbers.  Slick _does care_ about leading and trailing spaces in the names of the other layers, so be careful there maybe.  Slick could ignore these spaces too if you really wanted Slick to... but Slick really doesn't want to dictate more than Slick needs to.

Now, combine it all and Slick gets super slick, producing three files once again:

Cartoon.svg layers:
- (guides)
- --dialog--
  - English
  - French
  - German
- --speech bubbles--
  - English, French
  - German
- Background

Slick output:
- Cartoon_English.svg
- Cartoon_French.svg
- Cartoon_German.svg

### Bonus feature (sort of)

If your filename ends with `__master__` or `__MASTER__` or any case form such as `__MAsTer__`, Slick will strip this from the output filename.  For example, a source filename of `Cartoon__master__.svg` will still output the same filenames exampled above.  (But, who names a file like this other than me???)

## Installation

1. Download the latest release from the [Releases page](https://github.com/juanitogan/slick/releases).  (Or, any other way you like to git yer GitHub files.)  Be sure to choose the Slick release appropriate for your Inkscape version: v0.92.x, or v1.0 and later.

2. Unzip the INX and PY files to your Inkscape "User extensions" folder.  You can find that location in Inkscape here: Edit > Preferences > System.

3. Restart Inkscape.

4. Fin.  You'll find Slick here: Extensions > Export > SLiCk Layer Combinator.

## Example use of Slick

Because a picture is worth a thousand slicks... er... words.

Note the layer naming and layer hierarchies.  (I, personally, don't use the **!** convention as I'm just not the type to need it... yet.)

![SLiCk screenshot](https://github.com/juanitogan/slick/blob/master/readme-images/SLiCk%20screenshot.png)

Slick output:
- Car_0.svg
- Car_45.svg
- Car_90.svg
- Car_135.svg
- Car_180.svg
- Car_225.svg
- Car_270.svg
- Car_315.svg

## Pipeline automation

I didn't find any help on the net for command-line control of Inkscape extension scripts (the one's that require parameters like Slick does)... (why?) but, after reasoning it out, I eventually got it.  Here's an example DOS batch file:

### Inkscape 0.92

```batch
@echo off
pushd "C:\Program Files\Inkscape\share\extensions"
"C:\Program Files\Inkscape\python.exe" ^
  "%USERPROFILE%\AppData\Roaming\inkscape\extensions\slick_layer_combinator.py" ^
  -a true ^
  -d "C:\GRITS Racing\Art\Car" ^
  "C:\GRITS Racing\Art\Car\Car__master__.svg"
popd
```

Basically, what the above does is run Inkscape's copy of Python from Inkscape's `extensions` folder.  Python is required to run from here so that Slick's script can pick up the Inkscape packages needed to do Slick's thing.  Then, because this is running from a far-away folder in a far-away land, you must fully qualify the output directory and the master SVG file.

### Inkscape 1.0

```batch
@echo off
pushd "C:\Program Files\Inkscape\bin"
setlocal
set PYTHONPATH=C:\Program Files\Inkscape\share\inkscape\extensions
python ^
  "%USERPROFILE%\AppData\Roaming\inkscape\extensions\slick_layer_combinator.py" ^
  -a true ^
  -d "C:\GRITS Racing\Art\Car" ^
  "C:\GRITS Racing\Art\Car\Car__master__.svg"
endlocal
popd
```

Inkscape appears to be dead set on making this as hard to figure out as possible.  Now, (after hacking 1.0 for intel) it seems we have to run from the `bin` folder to find the DLLs and add Inkscape's `extensions` folder to the Python path.  Let's hope they don't change it up again.

**slick_layer_combinator.py** parameters:

```
-a, --all        (true|false)   Default: false. Find and export all option layers.
-l, --layers     "layer names"  Comma-separated list of option layers to export (if not using -a true).
-d, --directory  path           Path to save files to (supports ~ on Windows too).
```

All parameters are optional but you really need to specify `-d` if you don't want to go hunting for your files in some far-away folder.  Use either `-a` or `-l` if want a meaningful file output... otherwise, you'll get a `*_none.svg` file with all option layers hidden.

### Python warning!

Eeek!  A snake!  Due to a funky nuance of the Python language (that I won't bore you with the details of) you cannot end the output directory string with a backslash like so: `C:\GRITS Racing\Art\Car\`.  That really messes with the python's brain.  (Probably the fault of the writer of the OptionParser and arg_parser packages, really.)  So, leave off the final backslash like so: `C:\GRITS Racing\Art\Car`.  No worries, Slick is slick enough to add a slash if Slick can't find one.  If you must, you could end with a forward slash (slash direction doesn't matter with Slick) or a double backslash (weirdly enough).

## FAQ

**Q:** Can I use other layer hierarchies in my drawing?

**A:** Yes and no.  Be aware that the **()** and **!** conventions can appear at any level and will affect all children.  This is a good thing, I think.  If these are on an option layer, however, they are meaningless.  **Do not**, especially, create child layers under option layers, as they will be seen as more option layers and the results will likely be odd to you (and me).

**Q:** Why is SLiCk so fast compared to other extensions?

**A:** Because it is slick.

## To-do list

- Permutations.
  - Slick is not yet slick enough to process permutations.  Bugger.  If Slick ever is that slick, Slick will likely use a double-star convention (\*\*&nbsp;\*\*) much like the double-dash parent layers for options.  Permutations are scenarios like when you want all the layers in one permutation group to be combined one-by-one with all the layers in another permutation group (and/or with the non-permutating option layers).  There is a (much-more-boringly-named-:tongue:-although-"fluffware"-sounds-pretty-exciting-:wink:) tool that does this: [export_layer_combinations](https://github.com/fluffware/export_layer_combinations).  It outputs PNGs.
  - Hmm, like that other tool does, I may also need to add a group-identifier convention to allow a single permutation group to appear in more than one parent layer.  This could get messy real quick... which sounds very unslick.  Since this is likely to slip up artists that may not need such fancy-pantsiness, this is sounding a lot like this should be relegated to a spinoff tool.  Maybe called: _SLiP Layer Permutator_.
  - I, personally, have no need for automated permutations yet.  Thus, someone will need to talk me into building such a feature for when I get bored with all the other multiverse-improvement-attempting-but-often-failing-at-being-a-hero stuff I do.  I do have permutations of the example car art seen above but, currently, I handle them two other ways.  For example, that `(pilot)` layer could be split into two permutation layers called `Occupied` and `Unoccupied`.  But, instead of permutating out to 16 files versus 8 files, I just handle the pilot art with a single add-in sprite.  I also have car-damage permutations, but the art for the damage is so different that I choose to handle that scenario with a separate master file for each damage level.

- Consider an option to delete hidden layers (as mentioned earlier).

- Consider handling grandchildren of double-dash parent layers differently/better/slicker.

- Handle things better when budding artists choose to get really wild with commas and spaces.

- Slick wouldn't bother asking you for an output folder if Slick could determine your drawing's save location (assuming you've saved it first, which is not required) but, well, Inkscape isn't slick enough for Slick yet to allow such nonsense.  Come back to this if this ever changes.

### To-not-do list

- Add options for PNG export (and/or other formats).
  - Nope: Inkscape SVGs only.
  - Producing PNGs and such are what your pipeline scripts are for.  Of which, Slick is only just another slick tool in your slick toolset.
    - For example, after using Slick to generate a bunch of SVGs, you may then want to run a script that uses the [Inkscape command-line](https://wiki.inkscape.org/wiki/index.php?title=Using_the_Command_Line) to export a PNG for each.
    - It is also worth noting that [ImageMagick](https://imagemagick.org/) and [GIMP](https://www.gimp.org/) use the same rendering library (cairo/librsvg) for SVGs as Inkscape (while also noting cairo version differences and/or custom patches Inkscape may make to cairo).  I use ImageMagick in some of my scripts.  (ImageMagick also has a GhostScript rendering option, if really wanting something different than cairo, and less nice.)
    - Most of my SVGs, however, I can simply import into Unity 2017 via [SVG Importer](http://svgimporter.com/), which converts them to meshes.  Other tools can do similar mesh conversions.
    - Note to self: Blog about how to squeeze a bit more image quality out of PNGs with ImageMagick and oversampling.  Note also that Inkscape 1.0 PNG export now has a much-wanted antialiasing setting with a few quality options.

- Well, maybe add plain SVG export... um... nope.
