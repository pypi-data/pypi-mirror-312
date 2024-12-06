
# Table of Contents

1.  [CO2 monitor](#org5a19499)
2.  [Install](#orgc2c30e5)
    1.  [Development](#org989c74b)
3.  [Pins](#orgf82dd73)
    1.  [Screen](#org75b8d64)



<a id="org5a19499"></a>

# CO2 monitor

This project is more or less like [co2monitor.nl](https://co2monitor.nl), except that we show the current CO2 emisions per kWh of electricity on a small EPD screen, connected to some GPIO pins of a Raspberry Pi.

See [Pins](#orgf82dd73) for an overview of what pins need to be connected to the screen.


<a id="orgc2c30e5"></a>

# Install

1.  Attach your EPD screen to the pins as described in the table in [Screen](#org75b8d64).
2.  Install the python executable: `uv sync`, or `pip install -e .`
3.  Copy [.env.example](.env.example) to [.env](.env) and populate with the correct api key. You can find an api key on
    <https://ned.nl/nl/user>
4.  Run the executable (found in the virtualenv/bin directory).


<a id="org989c74b"></a>

## Development

See the [Makefile](Makefile) for handy dev commands. I use [uv](https://github.com/astral-sh/uv) to manage my dependencies, but it does not really matter all that much.

You can execute `python monitor` (or `uv run python monitor`) to quickly run the project.


<a id="orgf82dd73"></a>

# Pins

<https://pinout.xyz/>


<a id="org75b8d64"></a>

## Screen

[Product](https://www.waveshare.com/product/displays/e-paper/2.9inch-e-paper-module-b.htm)

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-right" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Name</th>
<th scope="col" class="org-left">Function</th>
<th scope="col" class="org-left">Color</th>
<th scope="col" class="org-right">Pin number</th>
<th scope="col" class="org-left">GPIO</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">VCC</td>
<td class="org-left">Power</td>
<td class="org-left">Grey</td>
<td class="org-right">1</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-left">GND</td>
<td class="org-left">Ground</td>
<td class="org-left">Brown</td>
<td class="org-right">6</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-left">DIN</td>
<td class="org-left">SPI MOSI</td>
<td class="org-left">Blue</td>
<td class="org-right">19</td>
<td class="org-left">10 (SPI0 MOSI)</td>
</tr>

<tr>
<td class="org-left">CLK</td>
<td class="org-left">SPI Clock</td>
<td class="org-left">Yellow</td>
<td class="org-right">23</td>
<td class="org-left">11 (SPI0 SCLK)</td>
</tr>

<tr>
<td class="org-left">CS</td>
<td class="org-left">SPI chip selection</td>
<td class="org-left">Orange</td>
<td class="org-right">24</td>
<td class="org-left">8  (SPI0 CE0)</td>
</tr>

<tr>
<td class="org-left">DC</td>
<td class="org-left">Data/Command selection</td>
<td class="org-left">Green</td>
<td class="org-right">22</td>
<td class="org-left">25</td>
</tr>

<tr>
<td class="org-left">RST</td>
<td class="org-left">Reset</td>
<td class="org-left">White</td>
<td class="org-right">11</td>
<td class="org-left">17</td>
</tr>

<tr>
<td class="org-left">BUSY</td>
<td class="org-left">Busy status output</td>
<td class="org-left">Purple</td>
<td class="org-right">18</td>
<td class="org-left">24</td>
</tr>
</tbody>
</table>

